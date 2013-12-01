from __future__ import print_function
import inspect
import pdb
import sys
import signal


def register(reg_signal=signal.SIGQUIT, reg_unhandled=True, commands=[]):
    """
    Registers exconsole hooks

    :param reg_signal: if not None, register signal handler (default: ``signal.SIGQUIT``)
    :param reg_unhandled: if ``True``, register unhandled exception hook (``sys.excepthook``)
    :param commands: list of custom commands/objects: (<local name>, <help string>, <function or object>)
    """
    if reg_signal:
        signal.signal(reg_signal, handle_quit)
    if reg_unhandled:
        sys.excepthook = handle_exception
    launch.commands = commands


def handle_exception(type, value, tb):
    launch(exception=value, extraceback=tb)


def handle_quit(signal, frame):
    launch(signalnum=signal, frame=frame)


def launch(exception=None, extraceback=None, signalnum=None, frame=None):
    """
    Launches an emergency console

    :param exception: unhandled exception value
    :param extraceback: unhandled exception traceback
    :param signalnum: interrupting signal number
    :param frame: interrupting signal frame
    """

    print('\n')
    print('Activating emergency console')
    print('----------------------------')

    print('Caused by:')
    if signalnum:
        signals = dict((k, v) for v, k in signal.__dict__.iteritems() if v.startswith('SIG'))
        print('Signal', signals.get(signalnum, 'unknown'))
    elif exception:
        print(exception.__class__.__name__)
        print(exception)
    else:
        print('manual invocation')

    stack = []
    locals = {}
    active_frame = 0
    if frame:
        current_frame = frame
        while current_frame:
            stack.insert(0, current_frame)
            current_frame = current_frame.f_back
    if extraceback:
        current_tb = extraceback
        while current_tb:
            stack.append(current_tb.tb_frame)
            current_tb = current_tb.tb_next

    import readline
    import code

    def _cmd_stack():
        index = 0
        print('\nStack frames:')
        for frame in stack:
            s = '> ' if (active_frame == index) else '  '
            s += '[%s] ' % str(index).rjust(3)
            lines, current_line = inspect.getsourcelines(frame)
            s += '%s:%i' % (inspect.getfile(frame), frame.f_lineno)
            s += '\n' + ' ' * 10
            if frame.f_lineno - current_line < len(lines):
                s += lines[frame.f_lineno - current_line].strip('\n')
            print(s)
            index += 1

    def _cmd_help():
        print((
            "Exconsole interactive emergency console\n"
            "Builtin commands:\n"
            " - _help()    this help\n"
            " - _s()       display stack\n"
            " - _f(index)  change current stack frame\n"
            " - _pdb()     launch PDB debugger\n"
            " - _exc       exception object\n"
            " - Ctrl-D     leave console\n"
        ))
        print('\n'.join(' - %s\t%s' % x[:2] for x in launch.commands))

    def _cmd_pdb():
        pdb.pm()

    def _cmd_frame(index):
        if not isinstance(index, int):
            print('index must be int')
            return
        if index < 0 or index >= len(stack):
            print('index out of bounds')
            return
        frame = stack[index] 
        locals.clear()
        locals.update(frame.f_locals)
        locals.update({
            '_help': _cmd_help,
            '_s': _cmd_stack,
            '_f': _cmd_frame,
            '_pdb': _cmd_pdb,
            '_exc': exception,
        })
        for command in launch.commands:
            locals[command[0]] = command[2]

        print('On frame %i' % index)
        print('Source:')

        lines, current_line = inspect.getsourcelines(frame)
        print(''.join(
            '    ' +
            ('>>' if lines.index(line) == frame.f_lineno - current_line else '  ') +
            ' ' + line
            for line in lines
        ))

    active_frame = len(stack) - 1
    _cmd_stack()
    _cmd_frame(len(stack) - 1)

    shell = code.InteractiveConsole(locals)

    print('Press Ctrl-D to leave console')
    print('Type "_help()" for built-in commands')

    shell.interact(banner='')
