# -*- coding: utf-8 -*-

# -- stdlib --
# -- third party --
# -- own --
from game.autoenv import EventHandler, Game, user_input
from gamepack.thb.actions import Damage, DrawCards, GenericAction, LaunchCard, UserAction
from gamepack.thb.actions import migrate_cards, user_choose_cards, user_choose_players
from gamepack.thb.cards import Attack, AttackCard, PhysicalCard, Skill, t_None
from gamepack.thb.characters.baseclasses import Character, register_character
from gamepack.thb.inputlets import ChooseOptionInputlet


# -- code --
class Echo(Skill):
    associated_action = None
    skill_category = ('character', 'passive')
    target = t_None


class EchoAction(UserAction):
    def __init__(self, source, target, card):
        self.source, self.target, self.card = source, target, card

    def apply_action(self):
        migrate_cards([self.card], self.target.cards, unwrap=True, is_bh=True)

        return True


class EchoHandler(EventHandler):
    interested = ('action_after',)

    def handle(self, evt_type, act):
        if evt_type == 'action_after' and isinstance(act, Damage):
            tgt = act.target
            if tgt.dead:
                return act

            if not tgt.has_skill(Echo):
                return act

            g = Game.getgame()
            pact = g.action_stack[-1]
            card = getattr(pact, 'associated_card', None)
            if not card or not card.is_card(PhysicalCard):
                return act

            if not card.detached or card.unwrapped:
                return act

            if not user_input([tgt], ChooseOptionInputlet(self, (False, True))):
                return act

            attack = card.is_card(AttackCard)
            pl = attack and user_choose_players(self, tgt, [p for p in g.players if not p.dead])
            p = pl[0] if pl else tgt

            g.process_action(EchoAction(tgt, p, card))

        return act

    def choose_player_target(self, tl):
        if not tl:
            return (tl, False)

        return (tl[-1:], True)


class Resonance(Skill):
    associated_action = None
    skill_category = ('character', 'passive')
    target = t_None


class ResonanceDrawAction(DrawCards):
    pass


class ResonanceLaunchCard(LaunchCard):
    pass


class ResonanceAction(GenericAction):
    card_usage = 'launch'

    def __init__(self, source, target, victim):
        self.source = source
        self.target = target
        self.victim = victim

    def apply_action(self):
        tgt, victim = self.target, self.victim
        cards = user_choose_cards(self, tgt, ('cards', 'showncards'))
        if not cards:
            return False

        c, = cards
        g = Game.getgame()
        g.process_action(ResonanceLaunchCard(tgt, [victim], c, bypass_check=True))

        return True

    def cond(self, cl):
        if len(cl) != 1:
            return False

        c = cl[0]
        if not c.associated_action:
            return False

        return issubclass(c.associated_action, Attack)

    def ask_for_action_verify(self, p, cl, tl):
        return ResonanceLaunchCard(self.source, [self.target], cl[0], bypass_check=True).can_fire()


class ResonanceHandler(EventHandler):
    interested = ('action_done',)

    def handle(self, evt_type, act):
        if evt_type == 'action_done' and isinstance(act, Attack):
            src = act.source
            tgt = act.target

            if src.dead or tgt.dead:
                return act

            if not src.has_skill(Resonance):
                return act

            g = Game.getgame()
            pl = [p for p in g.players if not p.dead and p not in (src, tgt)]

            if not pl:
                return act

            pl = user_choose_players(self, src, pl)

            if not pl:
                return act

            g.process_action(ResonanceAction(src, pl[0], tgt))

        return act

    def choose_player_target(self, tl):
        if not tl:
            return (tl, False)

        return (tl[-1:], True)


@register_character
class Kyouko(Character):
    skills = [Echo, Resonance]
    eventhandlers_required = [EchoHandler, ResonanceHandler]
    maxlife = 4
