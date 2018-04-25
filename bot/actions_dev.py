import re
from bot.player import Player
from bot.logger import logger

actions_dev = []


def fix_players_legs(self):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        self.tn.debuffplayer(player_object, "brokenLeg")
        self.tn.debuffplayer(player_object, "sprainedLeg")
        self.tn.send_message_to_player(player_object, "your legs have been taken care of ^^", color=self.bot.chat_colors['success'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("isequal", "fix my legs please", fix_players_legs, "(self)", "testing"))


def stop_the_bleeding(self):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        self.tn.debuffplayer(player_object, "bleeding")
        self.tn.send_message_to_player(player_object, "your wounds have been bandaided ^^", color=self.bot.chat_colors['success'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("isequal", "make me stop leaking", stop_the_bleeding, "(self)", "testing"))


def apply_first_aid(self):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        self.tn.buffplayer(player_object, "firstAidLarge")
        self.tn.send_message_to_player(player_object, "feel the power flowing through you!! ^^", color=self.bot.chat_colors['success'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("isequal", "heal me up scotty", apply_first_aid, "(self)", "testing"))


def make_player_admin(self):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        self.tn.set_admin_level(player_object, "2")
        self.tn.send_message_to_player(player_object, "and He said 'Let there be unlimited POWER!'. hit F1 and type cm <enter>, dm <enter>. exit console. press 'q' to fly, 'u' for items.", color=self.bot.chat_colors['success'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("isequal", "make me all powerful!", make_player_admin, "(self)", "testing"))


def reload_from_db(self):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        self.bot.load_from_db()
        self.tn.send_message_to_player(player_object, "loaded all from storage!", color=self.bot.chat_colors['success'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("isequal", "reinitialize", reload_from_db, "(self)", "testing"))


def shutdown_bot(self):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        self.tn.send_message_to_player(player_object, "bot is shutting down...", color=self.bot.chat_colors['success'])
        self.bot.shutdown_bot()
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("isequal", "shut down the matrix", shutdown_bot, "(self)", "testing"))


def obliterate_player(self):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        player_object.switch_off("suicide")
        self.tn.kick(player_object, "You wanted it! Time to be born again!!")
        location_objects_dict = self.bot.locations.get(player_object.steamid)
        locations_to_remove = []
        for name, location_object in location_objects_dict.iteritems():
            locations_to_remove.append(location_object)
        for location_object in locations_to_remove:
            self.bot.locations.remove(player_object.steamid, location_object.identifier)
            self.bot.players.remove(player_object)
            self.bot.whitelist.remove(player_object)
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("isequal", "obliterate me", obliterate_player, "(self)", "testing"))


def ban_player(self, command):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        p = re.search(r"ban\splayer\s(?P<steamid>.+)\sfor\s(?P<ban_reason>.+)", command)
        if p:
            steamid_to_ban = p.group("steamid")
            reason_for_ban = p.group("ban_reason")
            try:
                player_object_to_ban = self.bot.players.get(steamid_to_ban)
            except KeyError:
                player_dict = {'steamid': steamid_to_ban, "name": 'unknown offline player'}
                player_object_to_ban = Player(**player_dict)

            if self.tn.ban(player_object_to_ban, reason_for_ban):
                self.tn.send_message_to_player(player_object_to_ban, "you have been banned by {}".format(player_object.name), color=self.bot.chat_colors['alert'])
                self.tn.send_message_to_player(player_object, "you have banned player {}".format(steamid_to_ban), color=self.bot.chat_colors['success'])
                self.tn.say("{} has been banned by {} for '{}'!".format(steamid_to_ban, player_object.name, reason_for_ban), color=self.bot.chat_colors['success'])
            else:
                self.tn.send_message_to_player(player_object, "could not find a player with steamid {}".format(steamid_to_ban), color=self.bot.chat_colors['warning'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("startswith", "ban player", ban_player, "(self, command)", "testing"))


def unban_player(self, command):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        p = re.search(r"unban\splayer\s(?P<steamid>.+)", command)
        if p:
            steamid_to_unban = p.group("steamid")
            try:
                player_object_to_unban = self.bot.players.load(steamid_to_unban)
            except KeyError:
                player_dict = {'steamid': steamid_to_unban, "name": 'unknown offline player'}
                player_object_to_unban = Player(**player_dict)

            if self.tn.unban(player_object_to_unban):
                self.tn.send_message_to_player(player_object, "you have unbanned player {}".format(steamid_to_unban), color=self.bot.chat_colors['success'])
                self.tn.say("{} has been unbanned by {}.".format(steamid_to_unban, player_object.name), color=self.bot.chat_colors['success'])
            else:
                self.tn.send_message_to_player(player_object, "could not find a player with steamid {}".format(steamid_to_unban), color=self.bot.chat_colors['warning'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("startswith", "unban player", unban_player, "(self, command)", "testing"))


def kick_player(self, command):
    try:
        player_object = self.bot.players.get(self.player_steamid)
        p = re.search(r"kick\splayer\s(?P<steamid>.+)\sfor\s(?P<kick_reason>.+)", command)
        if p:
            steamid_to_kick = p.group("steamid")
            reason_for_kick = p.group("kick_reason")
            try:
                player_object_to_kick = self.bot.players.get(steamid_to_kick)
            except KeyError:
                self.tn.send_message_to_player(player_object, "could not find a player with steamid {}".format(steamid_to_kick), color=self.bot.chat_colors['warning'])
                return

            if self.tn.kick(player_object_to_kick, reason_for_kick):
                self.tn.send_message_to_player(player_object, "you have kicked {}".format(steamid_to_kick), color=self.bot.chat_colors['success'])
                self.tn.say("{} has been kicked by {} for '{}'!".format(steamid_to_kick, player_object.name, reason_for_kick), color=self.bot.chat_colors['success'])
    except Exception as e:
        logger.error(e)
        pass


actions_dev.append(("startswith", "kick player", kick_player, "(self, command)", "testing"))

