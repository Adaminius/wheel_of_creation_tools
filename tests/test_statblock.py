import pytest
import statblock
import utils


@pytest.fixture(scope='function')
def setup_statblock():
    with open('test_statblock.md') as file_handle:
        text = file_handle.read()
    return statblock.Statblock.from_markdown(text)


def test_statblock_md_parser(setup_statblock: statblock.Statblock):
    sb = setup_statblock
    assert sb.name == 'Test Name'
    assert sb.size == utils.size_name_to_val['Small']
    assert sb.primary_type == 'testType'
    assert sb.secondary_type == 'secondaryTestType'
    assert sb.alignment == 'testAlignment'
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
    assert len(sb.abilities) == 2
    assert sb.abilities[1].name == 'testAbility'
    assert sb.abilities[1].description_template == 'Foos bars.'
    assert sb.actions[1].name == 'Test Action'
    assert sb.bonus_actions[0].name == 'testBonusAction'
    assert sb.reactions[0].name == 'Test Reaction'
    assert sb.legendary_actions[0].name == 'Test Legendary Action'
    assert sb.num_legendary == 3
