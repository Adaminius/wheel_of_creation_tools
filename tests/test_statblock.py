import pytest
import statblock
import utils
import tags.woc_fey_means
import tags.woc_fey_mannerisms


@pytest.fixture(scope='function')
def setup_statblock():
    with open('test_statblock.md') as file_handle:
        text = file_handle.read()
    return statblock.Statblock.from_markdown(text)


def test_statblock_md_parser(setup_statblock: statblock.Statblock):
    utils.setup_logging(debug=True)

    sb = setup_statblock
    assert sb.name == 'Test Name'
    assert sb.size == utils.size_name_to_val['Small']
    assert sb.primary_type == 'testType'
    assert sb.secondary_type == 'secondaryTestType'
    assert sb.alignment == 'Unaligned'
    assert sb.armor_class == 12
    assert sb.armor_class_type == 'natural armor'
    assert sb.hit_points == 10
    assert sb.hit_dice.count == 2
    assert sb.hit_dice.size == 8
    assert sb.hit_point_bonus == 1
    assert sb.speed == 40
    assert sb.fly_speed == 30
    assert sb.swim_speed == 20
    assert sb.climb_speed == 10
    assert sb.ability_scores['STR'].value == 8
    assert sb.ability_scores['WIS'].value == 10
    assert sb.ability_scores['CHA'].value == 15
    assert sb.saving_throws['Int'] == 2
    assert sb.saving_throws['Cha'] == 3
    assert sb.skills['Perception'] == -2
    assert sb.skills['testSkill'] == 5
    assert sb.condition_immunities == ['testCondition', 'testCondition2']
    assert sb.blindsight == 10
    assert sb.tremorsense == 20
    assert sb.passive_perception == 8
    assert sb.languages == ['Sylvan', 'testLanguage']
    assert sb.telepathy == 100
    assert sb.challenge.rating == '1'
    assert len(sb.features) == 2
    assert sb.features[1].name == 'testAbility'
    assert sb.features[1].description_template == 'Foos bars.'
    assert sb.actions[1].name == 'Test Action'
    assert sb.bonus_actions[0].name == 'testBonusAction'
    assert sb.reactions[0].name == 'Test Reaction'
    assert sb.legendary_actions[0].name == 'Test Legendary Action'
    assert sb.num_legendary == 3
    assert 'testTag' in [t.name for t in sb.applied_tags]
    assert 'lithe' in [t.name for t in sb.applied_tags]


def test_apply_tags(setup_statblock: statblock.Statblock):
    utils.setup_logging(debug=True)

    sb = setup_statblock
    sb = tags.woc_fey_means.all_tags['lumbering'].apply(sb)
    assert sb.ability_scores['STR'].value == 10
    assert sb.speed == 35
    assert sb.fly_speed == 25
    assert sb.swim_speed == 15
    assert sb.climb_speed == 5
    assert tags.woc_fey_means.all_tags['lumbering'] in sb.applied_tags
    sb = tags.woc_fey_means.all_tags['Wintry'].apply(sb)
    assert sb.alignment == 'Winter'
    assert 'cold' in sb.damage_resistances
    assert 'psychic' in sb.damage_resistances
    assert tags.woc_fey_means.all_tags['Wintry'] in sb.applied_tags
    sb = tags.woc_fey_means.all_tags['Summery'].apply(sb)
    assert sb.alignment == 'Summer'
    assert 'fire' in sb.damage_resistances
    assert 'psychic' in sb.damage_resistances
    assert 'cold' not in sb.damage_resistances
    assert tags.woc_fey_means.all_tags['lumbering'] in sb.applied_tags
    assert tags.woc_fey_means.all_tags['Wintry'] not in sb.applied_tags
    assert tags.woc_fey_means.all_tags['Summery'] in sb.applied_tags
    assert len(sb.applied_tags) == 4
    sb = tags.woc_fey_means.all_tags['Wintry'].apply(sb)
    sb = tags.woc_fey_mannerisms.all_tags['cold logic'].apply(sb)
    assert len(sb.applied_tags) == 5
    # open('test_statblock_applied.md', 'w').write(sb.to_markdown())


def test_update_action_descriptions(setup_statblock: statblock.Statblock):
    sb = setup_statblock
    with open('test_statblock_updated.md', 'w') as file_handle:
        file_handle.write(sb.to_markdown())
    with open('test_statblock_updated.md') as file_handle:
        text = file_handle.read()
    sb_updated = statblock.Statblock.from_markdown(text)
    assert sb_updated.actions[1].description_template == 'Explodes for 3 (1d6 - 1) cold damage.'

