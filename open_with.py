import sublime
import sublime_plugin
import os
import json
import re


class OpenWithCommand(sublime_plugin.WindowCommand):
    def run(self):
        conf_path = os.path.join(sublime.packages_path(),
                                 'User',
                                 'SideBarEnhancements',
                                 'Open With',
                                 'Side Bar.sublime-menu')

        # This plugin uses the same configuration as SideBarEnhancements.
        if not os.path.exists(conf_path):
            sublime.error_message('Cannot find {0}. Be sure you have SideBarEnhancements plugin installed.'.format(conf_path))
            return

        f = open(conf_path, 'r')
        data = f.read()
        f.close()

        # Python json library does not like comments in json.
        data = re.sub(r'//.*', '', data)
        conf = json.loads(data, strict=False)

        labels = []
        items = []

        for item in conf:
            if item['id'] == 'side-bar-files-open-with':
                for child in item['children']:
                    caption = child['caption']
                    if caption != '-':
                        items.append(child)
                        labels.append(child['caption'])

        def on_item_chosen(index):
            if index is not -1:
                item = items[index]
                self.window.run_command(item['command'], item['args'])

        self.window.show_quick_panel(labels,
                                     on_item_chosen)
