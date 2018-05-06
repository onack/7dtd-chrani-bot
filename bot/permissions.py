from assorted_functions import byteify
import json
import os

from bot.command_line_args import args_dict


class Permissions(object):

    root = str
    prefix = str

    player_actions_list = list
    permission_levels_list = list
    action_permissions_dict = dict

    available_actions_dict = dict

    def __init__(self, player_actions_list, permission_levels_list):
        self.root = 'data/permissions'
        self.prefix = args_dict['Database-file']
        self.permission_levels_list = permission_levels_list
        self.player_actions_list = player_actions_list
        self.available_actions_dict = {}
        self.action_permissions_dict = {}

    def player_has_permission(self, player_object, action_identifier=None, action_group=None):
        if action_group is None:
            for group in self.action_permissions_dict.iteritems():
                pass
        if isinstance(action_group, str):
            try:
                allowed_player_groups = self.action_permissions_dict[action_group][action_identifier]
                if any((True for x in player_object.permission_levels if x in allowed_player_groups)) is True:
                    return True
                else:
                    return allowed_player_groups
            except (KeyError, TypeError):
                return False  # for now

    def load_all(self):
        filename = "{}/{}_permissions.json".format(self.root, self.prefix)
        try:
            with open(filename) as file_to_read:
                self.action_permissions_dict = byteify(json.load(file_to_read))
        except IOError:  # no permissions file available
            pass

        self.update_permissions_file()

    def update_permissions_file(self):
        filename = '{}/{}_permissions.json'.format(self.root, self.prefix)

        available_actions_dict = {}
        for player_action in self.player_actions_list:
            if (len(player_action) == 5): # quick hack to get some system-functions in ^^
                # if it were '6', it would be a system action not requiring permission, they are available to all
                try:
                    # see if this exact action already has permission groups attached
                    permission_groups = self.action_permissions_dict[player_action[4]][getattr(player_action[2], 'func_name')]
                except KeyError:
                    permission_groups = None

                try:
                    # permission group already exists, update it
                    available_actions_dict[player_action[4]].update({getattr(player_action[2], 'func_name'): permission_groups})
                except Exception:
                    # the whole permission group is new, set it up!
                    available_actions_dict[player_action[4]] = {getattr(player_action[2], 'func_name'): permission_groups}
        try:
            self.save(available_actions_dict)
            return filename
        except Exception:
            raise IOError

    def save(self, available_actions_dict):
        dict_to_save = available_actions_dict
        filename = '{}/{}_permissions.json'.format(self.root, self.prefix)
        with open(filename, 'w+') as file_to_write:
            json.dump(dict_to_save, file_to_write, indent=4)
