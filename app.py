import importlib
import importlib.util
import os
import statblock
import utils
from glob import glob
from flask import Flask
from flask import request
from flask_cors import CORS
from jinja2 import Template


DEBUG = True
modules = {}
app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    with open('templates/index.html') as file_handle:
        text = file_handle.read()
    return text


@app.route('/getTagList', methods=['GET'])
def get_tag_list():
    # spec = importlib.util.spec_from_file_location('modulename', filename)
    # module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(module)  # should already be loaded, but let's reload so we can edit on the fly
    # importlib.reload(filename)
    filename = request.args.get('filename')
    template = Template(
        """<tr onclick="selectTag('{{ filename }}', '{{ tag_name }}' data-toggle="tooltip" title="Add this tag">
             <td>{{ weight }}</td>
             <td><strong>{{ tag_name }}</strong></td>
             <td>{{ effect }}</td>
           </tr>
        """
    )
    out = ''
    for name, tag_dict in statblock.Tag.get_dict_table(modules[filename].all_tags).items():
        out += template.render(filename=filename, tag_name=name, weight=tag_dict['weight'], effect=tag_dict['effect'])
    return out


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
    for filename in filenames:
        if modules.get(filename) is None:
            spec = importlib.util.spec_from_file_location('modulename', filename)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[os.path.basename(filename)] = module
        else:
            module = modules[filename]
            if DEBUG:
                importlib.reload(module)
        out += template.render(filename=os.path.basename(filename), table_name=module.table_name)
    return out

@app.route('/getAllStatblocks', methods=['GET'])
def get_all_statblocks():
    """Returns filename for each statblock in statblocks/ as HTML"""
    filenames = glob('statblocks/*py')
    template = Template(
        """<a class="dropdown-item" style="cursor: pointer;" onclick="selectStatblock('{{ filename }}')">
          {{ filename }}
        </a>"""
    )
    out = ''
    for filename in filenames:
        out += template.render(filename=os.path.basename(filename))
    return out


if __name__ == '__main__':
    app.run()
