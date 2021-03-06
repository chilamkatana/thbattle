# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
# -- own --
from gamepack.thb import cards, characters
from gamepack.thb.ui.ui_meta.common import gen_metafunc, passive_clickable, passive_is_action_valid

# -- code --
__metaclass__ = gen_metafunc(characters.nazrin)


class Nazrin:
    # Character
    char_name = u'纳兹琳'
    port_image = 'thb-portrait-nazrin'
    miss_sound_effect = 'thb-cv-nazrin_miss'
    description = (
        u'|DB探宝的小小大将 纳兹琳 体力：3|r\n\n'
        u'|G轻敏|r:你可以将一张黑色手牌当【擦弹】使用或打出。\n\n'
        u'|G探宝|r:准备阶段开始时，你可以进行一次判定，若结果为黑色，你获得此牌，你可以重复此流程，直到出现红色的判定结果为止。\n\n'
        u'|DB（画师：Pixiv ID 3378132，CV：小羽）|r'
    )


class NazrinKOF:
    # Character
    char_name = u'纳兹琳'
    port_image = 'thb-portrait-nazrin'
    miss_sound_effect = 'thb-cv-nazrin_miss'
    description = (
        u'|DB探宝的小小大将 纳兹琳 体力：3|r\n\n'
        u'|G轻敏|r:你可以将一张|B黑桃|r色手牌当【擦弹】使用或打出。\n\n'
        u'|G探宝|r:准备阶段开始时，你可以进行一次判定，若结果为黑色，你获得此牌，你可以重复此流程，直到出现红色的判定结果为止。\n\n'
        u'|RKOF修正角色|r\n\n'
        u'|DB（画师：Pixiv ID 3378132，CV：小羽）|r'
    )


class TreasureHunt:
    # Skill
    name = u'探宝'
    clickable = passive_clickable
    is_action_valid = passive_is_action_valid


class TreasureHuntHandler:
    # choose_option
    choose_option_buttons = ((u'发动', True), (u'不发动', False))
    choose_option_prompt = u'你要发动【探宝】吗？'


class Agile:
    # Skill
    name = u'轻敏'

    def clickable(game):
        me = game.me

        try:
            act = game.action_stack[-1]
        except IndexError:
            return False

        if isinstance(act, cards.BaseUseGraze) and (me.cards or me.showncards):
            return True

        return False

    def is_complete(g, cl):
        skill = cl[0]
        cl = skill.associated_cards
        if len(cl) != 1:
            return (False, u'请选择一张牌！')
        else:
            c = cl[0]
            if c.resides_in not in (g.me.cards, g.me.showncards):
                return (False, u'请选择手牌！')
            if c.suit not in (cards.Card.SPADE, cards.Card.CLUB):
                return (False, u'请选择一张黑色的牌！')
            return (True, u'这种三脚猫的弹幕，想要打中我是不可能的啦~')

    def sound_effect(act):
        return 'thb-cv-nazrin_agile'


class AgileKOF:
    # Skill
    name = u'轻敏'

    clickable = Agile['clickable']

    def is_complete(g, cl):
        skill = cl[0]
        cl = skill.associated_cards
        if len(cl) != 1:
            return (False, u'请选择一张牌！')
        else:
            c = cl[0]
            if c.resides_in not in (g.me.cards, g.me.showncards):
                return (False, u'请选择手牌！')
            if c.suit != cards.Card.SPADE:
                return (False, u'请选择一张黑桃色手牌牌！')
            return (True, u'这种三脚猫的弹幕，想要打中我是不可能的啦~')

    sound_effect = Agile['sound_effect']


class TreasureHuntAction:
    fatetell_display_name = u'探宝'

    def effect_string(act):
        if act.succeeded:
            return u'|G【%s】|r找到了|G%s|r' % (
                act.target.ui_meta.char_name,
                act.card.ui_meta.name,
            )
        else:
            return u'|G【%s】|r什么也没有找到…' % (
                act.target.ui_meta.char_name,
            )

    def sound_effect(act):
        tgt = act.target
        t = tgt.tags
        if not t['__treasure_hunt_se'] >= t['turn_count']:
            t['__treasure_hunt_se'] = t['turn_count']
            return 'thb-cv-nazrin_treasurehunt'
