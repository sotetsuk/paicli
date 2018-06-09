"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import unicode_literals
from prompt_toolkit.application import Application
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.filters import IsDone
from prompt_toolkit.layout.controls import TokenListControl
from prompt_toolkit.layout.containers import ConditionalContainer, ScrollOffsets, HSplit
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict

# Reference
#
# examples/custom-token-list-control.py:
# https://github.com/jonathanslenders/python-prompt-toolkit/pull/427/commits/2b75d1835eee49c8881c1d8d7e107237227eda95#diff-a4228333fe0e9eca1e3149e15ae2d8de
#

string_query = ' Command Select '
inst = 'Choose the job'


def select_job_interactively(job_content):
    choices = [job['name'] for job in job_content]
    app = get_app(choices)

    eventloop = create_eventloop()
    try:
        cli = CommandLineInterface(application=app, eventloop=eventloop)
        selected_job = cli.run(reset_current_buffer=False)
    finally:
        eventloop.close()

    return selected_job


def get_app(choices):

    class InquirerControl(TokenListControl):
        selected_option_index = 0
        answered = False
        choices = []
    
        def __init__(self, choices, **kwargs):
            self.choices = choices
            super(InquirerControl, self).__init__(self._get_choice_tokens, **kwargs)
    
        @property
        def choice_count(self):
            return len(self.choices)
    
        def _get_choice_tokens(self, cli):
            tokens = []
            T = Token
    
            def append(index, label):
                selected = (index == self.selected_option_index)
                tokens.append((T.Selected if selected else T, '> ' if selected else '  '))
                if selected:
                    tokens.append((Token.SetCursorPosition, ''))
                tokens.append((T.Selected if selected else T, '%-24s' % label))
                tokens.append((T, '\n'))
    
            for i, choice in enumerate(self.choices):
                append(i, choice)
            tokens.pop()  # Remove last newline.
            return tokens
    
        def get_selection(self):
            return self.choices[self.selected_option_index]

    ic = InquirerControl(choices)

    def get_prompt_tokens(cli):
        tokens = []
        if ic.answered:
            cli.return_value = lambda: ic.get_selection()
        return tokens
    
    layout = HSplit([
        Window(height=D.exact(0),
               content=TokenListControl(get_prompt_tokens, align_center=False)),
        ConditionalContainer(
            Window(
                ic,
                width=D.exact(43),
                height=D(min=3),
                scroll_offsets=ScrollOffsets(top=1, bottom=1)
            ),
            filter=~IsDone())])
    
    manager = KeyBindingManager.for_prompt()
    
    @manager.registry.add_binding(Keys.ControlQ, eager=True)
    @manager.registry.add_binding(Keys.ControlC, eager=True)
    def _(event):
        event.cli.set_return_value(None)
    
    @manager.registry.add_binding(Keys.Down, eager=True)
    @manager.registry.add_binding(Keys.ControlN, eager=True)
    def move_cursor_down(event):
        ic.selected_option_index = (
                (ic.selected_option_index + 1) % ic.choice_count)
    
    @manager.registry.add_binding(Keys.Up, eager=True)
    @manager.registry.add_binding(Keys.ControlP, eager=True)
    def move_cursor_up(event):
        ic.selected_option_index = (
                (ic.selected_option_index - 1) % ic.choice_count)
    
    @manager.registry.add_binding(Keys.Enter, eager=True)
    def set_answer(event):
        ic.answered = True
        event.cli.set_return_value(None)
    
    inquirer_style = style_from_dict({
        Token.QuestionMark: '#5F819D',
        Token.Selected: '#FF9D00',
        Token.Instruction: '',
        Token.Answer: '#FF9D00 bold',
        Token.Question: 'bold',
    })
    
    app = Application(
        layout=layout,
        key_bindings_registry=manager.registry,
        mouse_support=True,
        style=inquirer_style
    )

    return app


