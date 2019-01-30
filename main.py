import importlib
import importlib.util
import sys
import pprint
import statblock
import utils
import markdown as md
import re
import json
from os.path import basename
from glob import glob
from flask import Flask
from flask import request
from flask_cors import CORS
from jinja2 import Template


DEBUG = True
modules = {}
app = Flask(__name__)
CORS(app)


def load_tag_module(filename):
    filename = basename(filename)
    spec = importlib.util.spec_from_file_location(filename.split('.')[0], 'tags/{}'.format(filename))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    modules[filename] = module
    print('loaded {}: {}'.format(filename, module))


@app.route('/')
def home():
    with open('templates/index.html') as file_handle:
        template = Template(file_handle.read())
    with open('statblocks/quadruped_predator.md') as file_handle:
        markdown_text = file_handle.read()
    preview_html = md.markdown(prepare_markdown(markdown_text), extensions=['tables'])
    return template.render(prefill_preview=preview_html, prefill_md=markdown_text)

@app.route('/getStatblock', methods=['GET'])
def get_statblock():
    filename = request.args.get('filename')
    with open('statblocks/{}'.format(filename)) as file_handle:
        text = file_handle.read()
    return text

@app.route('/getTagList', methods=['GET'])
def get_tag_list():
    filename = request.args.get('filename')
    if modules.get(basename(filename)) is None:
        load_tag_module(filename)

    template = Template(
        """<tr onclick="selectTag('{{ filename }}', '{{ tag_name }}', '{{ stacks }}')" 
        data-toggle="tooltip" title="stacks={{ stacks }}" data-name="{{ tag_name }}" data-filename="{{ filename }}"
        data-weight="{{ weight }}" data-stacks="{{ stacks }}" data-requires="{{ requires }}">
             <td>{{ weight }}</td>
             <td><strong>{{ tag_name }}</strong></td>
             <td>{{ effect }}</td>
             <td>{{ requires }}</td>
           </tr>
        """
    )
    out = ''
    for name, tag_dict in statblock.Tag.get_dict_table(modules[basename(filename)].all_tags).items():
        requires = ','.join(tag_dict['requires']) if tag_dict['requires'] else '-'
        out += template.render(filename=filename, tag_name=name, weight=tag_dict['weight'], effect=tag_dict['effect'],
                               stacks=tag_dict['stacks'], requires=requires)

    description_template = """<div class="card"  style="margin-top: 1rem; margin-bottom: 1rem;">
          <div class="card-header" id="headingTagDesc">
            <h5 class="mb-0">
              <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapseTagDesc" aria-expanded="false" aria-controls="collapseTagDesc">
                {{ table_name }}
              </button>
            </h5>
          </div>

          <div id="collapseTagDesc" class="collapse hide" aria-labelledby="headingTagDesc">
            <div class="card-body">{{ description }}</p>
            </div>
          </div>
        </div>"""
    description_template = Template(description_template)
    description = description_template.render(table_name=modules[basename(filename)].table_name,  # todo set a variable to the module instead of looking it up 3 times, setup default values
                                              description=modules[basename(filename)].table_description)
    return json.dumps({'tags': out, 'description': description})


@app.route('/getAllTagLists', methods=['GET'])
def get_all_tag_lists() -> str:
    """Returns the 'table_name' from each module in tags/ as HTML"""
    # <a class="dropdown-item" onclick="selectTagList()" href="#">Action</a>
    template = Template(
        """<a class="dropdown-item" style="cursor: pointer;" onclick="selectTagList('{{ filename }}')">
          {{ table_name }}
        </a>"""
    )
    out = ''
    filenames = glob('tags/*py')

    # put WoC filenames first
    woc_filenames = sorted([filename for filename in filenames if 'woc' in filename.lower()])
    not_woc_filenames = sorted([filename for filename in filenames if 'woc' not in filename.lower()])
    filenames = woc_filenames + not_woc_filenames

    for filename in filenames:
        if modules.get(filename) is None or DEBUG:
            load_tag_module(filename)
        module = modules[basename(filename)]
        out += template.render(filename=basename(filename), table_name=module.table_name)
    return out

@app.route('/getAllStatblocks', methods=['GET'])
def get_all_statblocks():
    """Returns filename for each statblock in statblocks/ as HTML"""
    filenames = glob('statblocks/*md')
    template = Template(
        """<a class="dropdown-item" style="cursor: pointer;" onclick="selectStatblock('{{ filename }}')">
          {{ filename }}
        </a>"""
    )
    out = ''
    for filename in filenames:
        out += template.render(filename=basename(filename))
    return out

def prepare_markdown(text: str) -> str:
    text = re.sub('___\s+___\n', '', text)
    text = re.sub('> ___', '\n> ___\n', text)
    text = text.replace('>', '> ')
    text = text.replace('>  ', '> ')
    return text

@app.route('/modifyStatblock', methods=['POST', 'GET'])
def get_modified_statblock():
    data = request.get_json()
    sb = statblock.Statblock.from_markdown(text=data['statblock'])
    for tag in data['tags[]']:
        print(tag['name'], tag['filename'])
        if modules.get(tag['filename']) is None:
            load_tag_module(tag['filename'])
        sb = modules[basename(tag['filename'])].all_tags[tag['name']].apply(sb)

    markdown_text = sb.to_markdown()
    preview_html = md.markdown(prepare_markdown(markdown_text), extensions=['tables'])

    return json.dumps({'markdown': markdown_text, 'html': preview_html})

if __name__ == '__main__':
    app.run()
