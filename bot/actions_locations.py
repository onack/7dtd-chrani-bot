import re
from bot.location import Location

actions_locations = []


def set_up_location(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"set up a location named (.+)", command)
        if p:
            name = p.group(1)
            location_object = Location()
            location_object.set_name(name)
            identifier = location_object.set_identifier(name)  # generate the identifier from the name
            location_object.set_owner(player_object.steamid)
            location_object.set_shape("sphere")
            location_object.set_coordinates(player_object)
            location_object.set_region([player_object.region])
            # TODO: this seems like a crappy solution ^^ need a way more elegant... way
            messages_dict = location_object.get_messages_dict()
            messages_dict["entering_core"] = "entering {}'s core".format(name)
            messages_dict["leaving_core"] = "leaving {}'s core".format(name)
            messages_dict["entering_boundary"] = "entering {}".format(name)
            messages_dict["leaving_boundary"] = "leaving {}".format(name)
            location_object.set_messages(messages_dict)
            location_object.set_list_of_players_inside([player_object.steamid])
            self.bot.locations.upsert(location_object, save=True)
            self.tn.send_message_to_player(player_object, "You have created a location, it is stored as {} and spans {} meters.".format(identifier, int(location_object.radius * 2)), color='22c927')
            self.tn.send_message_to_player(player_object, "use {} to access it with commands like /set up name for {} as Whatever the name shall be".format(identifier, identifier), color='22c927')
    else:
        self.tn.send_message_to_player(player_object, "{} is no authorized no nope. should go read read!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "set up a location named", set_up_location, "(self, command)", "locations"))


def set_up_location_teleport(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"set up teleport for location (.+)", command)
        if p:
            identifier = p.group(1)
            try:
                location_object = self.bot.locations.get(player_object.steamid, identifier)
            except KeyError:
                self.tn.send_message_to_player(player_object, "coming from the wrong end... set up the location first!", color='db500a')
                return False

            if location_object.set_teleport_coordinates(player_object):
                self.bot.locations.upsert(location_object, save=True)
                self.tn.send_message_to_player(player_object, "the teleport for {} has been set up!".format(identifier), color='22c927')
            else:
                self.tn.send_message_to_player(player_object, "your position seems to be outside the location", color='db500a')

    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "set up teleport for location", set_up_location_teleport, "(self, command)", "locations"))


def name_my_location(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"set up the name for location (.+)\sas\s(.+)", command)
        if p:
            identifier = p.group(1)
            name = p.group(2)
            try:
                location_object = self.bot.locations.get(player_object.steamid, identifier)
                location_object.set_name(name)
                messages_dict = location_object.get_messages_dict()
                messages_dict["entering_core"] = "entering {}'s core area ".format(name)
                messages_dict["leaving_core"] = "leaving {}'s core area ".format(name)
                messages_dict["entering_boundary"] = "entering {} ".format(name)
                messages_dict["leaving_boundary"] = "leaving {} ".format(name)
                location_object.set_messages(messages_dict)
                self.bot.locations.upsert(location_object, save=True)
                self.tn.say("{} called a location {}".format(player_object.name, name), color='22c927')
            except KeyError:
                self.tn.send_message_to_player(player_object, "You can not name that which you do not have!!", color='db500a')

    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "set up the name for location", name_my_location, "(self, command)", "locations"))


def set_up_location_boundary(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"set up the boundary for location (.+)", command)
        if p:
            identifier = p.group(1)
            try:
                location_object = self.bot.locations.get(player_object.steamid, identifier)
            except KeyError:
                self.tn.send_message_to_player(player_object, "I can not find a location called {}".format(identifier), color='db500a')
                return False

            set_radius, allowed_range = location_object.set_radius(player_object)
            if set_radius is True:
                self.bot.locations.upsert(location_object, save=True)
                self.tn.send_message_to_player(player_object, "the location {} ends here and spans {} meters ^^".format(identifier, int(location_object.radius * 2)), color='22c927')
            else:
                self.tn.send_message_to_player(player_object, "you given radius of {} seems to be invalid, allowed radius is {} to {} meters".format(int(set_radius), int(allowed_range[0]), int(allowed_range[-1])), color='db500a')

    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "set up the boundary for location ", set_up_location_boundary, "(self, command)", "locations"))


def set_up_location_area(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"set up the location (.+) as a room starting from south west going north (.+)and east (.+) and up (.+)", command)
        if p:
            identifier = p.group(1)
            length = p.group(2)
            width = p.group(3)
            height = p.group(4)
            try:
                location_object = self.bot.locations.get(player_object.steamid, identifier)
            except KeyError:
                self.tn.send_message_to_player(player_object, "I can not find a location called {}".format(identifier), color='db500a')
                return False

            set_width, allowed_range = location_object.set_width(width)
            set_length, allowed_range = location_object.set_length(length)
            set_height, allowed_range = location_object.set_height(height)
            if set_width is True and set_length is True and set_height is True:
                location_object.set_shape("room")
                location_object.set_center(player_object, location_object.width, location_object.length, location_object.height)
                self.bot.locations.upsert(location_object, save=True)
                self.tn.send_message_to_player(player_object, "the location {} ends here and spans {} meters ^^".format(identifier, int(location_object.radius * 2)), color='22c927')
            else:
                self.tn.send_message_to_player(player_object, "you given coordinates seem to be invalid", color='db500a')

    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "set up the location", set_up_location_area, "(self, command)", "locations"))


def set_up_location_warning_boundary(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"set up a warning boundary for location (.+)", command)
        if p:
            identifier = p.group(1)
            try:
                location_object = self.bot.locations.get(player_object.steamid, identifier)
            except KeyError:
                self.tn.send_message_to_player(player_object, "I can not find a location called {}".format(identifier), color='db500a')
                return False

            set_radius, allowed_range = location_object.set_warning_boundary(player_object)
            if set_radius is True:
                self.bot.locations.upsert(location_object, save=True)
                self.tn.send_message_to_player(player_object, "the warning boundary {} ends here and spans {} meters ^^".format(identifier, int(location_object.warning_boundary * 2)), color='22c927')
            else:
                self.tn.send_message_to_player(player_object, "you given radius of {} seems to be invalid, allowed radius is {} to {} meters".format(int(set_radius), int(allowed_range[0]), int(allowed_range[-1])), color='db500a')

    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "set up a warning boundary for location ", set_up_location_warning_boundary, "(self, command)", "locations"))


def make_location_a_shape(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    p = re.search(r"make the location (.+) a (.+)", command)
    if p:
        name = p.group(1)
        shape = p.group(2)
        if player_object.authenticated is True:
            try:
                location_object = self.bot.locations.get(player_object.steamid, name)
                if location_object.set_shape(shape):
                    self.bot.locations.upsert(location_object, save=True)
                    self.tn.send_message_to_player(player_object, "{} is a {} now.".format(location_object.name, shape), color='22c927')
                else:
                    self.tn.send_message_to_player(player_object, "{} is not an allowed shape at this time!".format(shape), color='db500a')
                    return False

            except KeyError:
                self.tn.send_message_to_player(player_object, "You can not change that which you do not own!", color='db500a')
        else:
            self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "make the location", make_location_a_shape, "(self, command)", "locations"))


def list_players_locations(self):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        try:
            location_objects_dict = self.bot.locations.get(player_object.steamid)
            for name, location_object in location_objects_dict.iteritems():
                self.tn.send_message_to_player(player_object, "{} @ ({} x:{}, y:{}, z:{})".format(location_object.name, location_object.identifier, location_object.pos_x, location_object.pos_y, location_object.pos_z))

        except KeyError:
            self.tn.send_message_to_player(player_object, "{} can not list that which he does not have!".format(player_object.name), color='db500a')
    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("isequal", "list my locations", list_players_locations, "(self)", "locations"))


def goto_location(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"goto location\s(.+)", command)
        if p:
            name = p.group(1)
            try:
                location_object = self.bot.locations.get(player_object.steamid, name)
                self.tn.say("{} went to location {}".format(player_object.name, name), color='22c927')
                self.tn.teleportplayer(player_object, location_object)
            except KeyError:
                self.tn.send_message_to_player(player_object, "i have never heard of {}".format(name), color='db500a')

    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "goto location", goto_location, "(self, command)", "locations"))


def remove_location(self, command):
    player_object = self.bot.players.get(self.player_steamid)
    if player_object.authenticated is True:
        p = re.search(r"remove location\s(.+)", command)
        if p:
            identifier = p.group(1)
            try:
                location_object = self.bot.locations.get(player_object.steamid, identifier)
                self.bot.locations.remove(player_object.steamid, identifier)
                self.tn.say("{} deleted location {}".format(player_object.name, identifier), color='22c927')
            except KeyError:
                self.tn.send_message_to_player(player_object, "i have never heard of {}".format(identifier), color='db500a')

    else:
        self.tn.send_message_to_player(player_object, "{} needs to enter the password to get access to sweet commands!".format(player_object.name), color='db500a')


actions_locations.append(("startswith", "remove location", remove_location, "(self, command)", "locations"))
"""
here come the observers
"""
observers_locations = []


def player_crossed_boundary(self):
    player_object = self.bot.players.get(self.player_steamid)
    for location_owner_steamid in self.bot.locations.locations_dict:
        """ go through each location and check if the player is inside
        locations are stored on a player-basis so we can have multiple 'home' and 'spawn' location and whatnot
        so we have to loop through every player_location_dict to get to the actual locations
        """
        for location_name, location_object in self.bot.locations.locations_dict[location_owner_steamid].iteritems():
            """ different status-conditions for a player
            None = do nothing
            is inside
            has entered
            has left
            """
            get_player_status = location_object.get_player_status(player_object)
            if get_player_status is None:
                pass
            if get_player_status == "is inside":
                pass
            if get_player_status == "has left":
                if location_object.messages_dict["leaving_boundary"] is not None:
                    self.tn.send_message_to_player(player_object, location_object.messages_dict["leaving_boundary"])
                self.bot.locations.upsert(location_object, save=True)
            if get_player_status == "has entered":
                if location_object.messages_dict["entering_boundary"] is not None:
                    self.tn.send_message_to_player(player_object, location_object.messages_dict["entering_boundary"], color='db500a')
                self.bot.locations.upsert(location_object, save=True)


observers_locations.append(("player crossed boundary", player_crossed_boundary, "(self)"))
