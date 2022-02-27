import PySimpleGUI as sg
import sqlite3

frame1 = sg.Frame('INPUT',
                  [
                      [

                          sg.Input('', size=(50, 1), key='-TEXT-'),
                          sg.Button('PUSH', size=(5, 1), key='-BUTTON-'),
                          sg.Button('x', size=(2, 1), key='-X-')
                      ]
                  ], size=(460, 50)
                  )

frame2 = sg.Frame('TASK',
                  [
                      [

                          sg.Input('', size=(50, 1), key='-INPUT0-'),
                          sg.Button('EDIT', size=(5, 1), key='-EDIT0-'),
                          sg.Button('X', size=(2, 1), key='-X0-')
                      ],
                      [

                          sg.Input('', size=(50, 1), key='-INPUT1-'),
                          sg.Button('EDIT', size=(5, 1), key='-EDIT1-'),
                          sg.Button('X', size=(2, 1), key='-X1-')
                      ],
                      [

                          sg.Input('', size=(50, 1), key='-INPUT2-'),
                          sg.Button('EDIT', size=(5, 1), key='-EDIT2-'),
                          sg.Button('X', size=(2, 1), key='-X2-')
                      ],
                      [

                          sg.Input('', size=(50, 1), key='-INPUT3-'),
                          sg.Button('EDIT', size=(5, 1), key='-EDIT3-'),
                          sg.Button('X', size=(2, 1), key='-X3-')
                      ],
                      [

                          sg.Input('', size=(50, 1), key='-INPUT4-'),
                          sg.Button('EDIT', size=(5, 1), key='-EDIT4-'),
                          sg.Button('X', size=(2, 1), key='-X4-')
                      ],

                  ], size=(460, 200)
                  )

layout = [
    [
        frame1
    ],
    [
        sg.Text('', key='-INFO-', text_color='red')
    ],
    [
        frame2
    ]
]

window = sg.Window(title='Todo', layout=layout)
window.finalize()


def task_rendering(cur):
    window['-INPUT0-'].update('')
    window['-INPUT1-'].update('')
    window['-INPUT2-'].update('')
    window['-INPUT3-'].update('')
    window['-INPUT4-'].update('')
    count = 0
    for row in cur.execute('SELECT * FROM todos'):
        if count > 4:
            break
        else:
            row = ''.join(row)
            window['-INPUT' + str(count) + '-'].update(row)
            count = count + 1


def db_edit(num):
    print("EDIT", num)
    # sg.popup_get_text('{}'.format(values['-INPUT' + str(num) + '-']))


def db_delete(num):
    con = sqlite3.connect('todo.db')
    cur = con.cursor()
    val = values['-INPUT' + str(num) + '-']
    val = tuple([val])
    cur.execute('DELETE FROM todos WHERE text = ?', val)
    con.commit()
    task_rendering(cur)
    con.close()


def db_add():
    con = sqlite3.connect('todo.db')
    cur = con.cursor()
    val = [values['-TEXT-']]
    cur.execute("INSERT INTO todos VALUES(?)", val)
    con.commit()
    task_rendering(cur)
    con.close()


def db_init():
    con = sqlite3.connect('todo.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS todos(text TEXT)''')
    task_rendering(cur)
    con.close()


db_init()
while True:
    event, values = window.read(timeout=None)
    if event is None:
        break
    if event == '-BUTTON-':
        if values['-TEXT-'] == '':
            window['-INFO-'].update('ERROR!')
        else:
            db_add()
            window['-TEXT-'].update('')

    if event == '-EDIT0-':
        if values['-INPUT0-'] == '':
            window['-INFO-'].update('ERROR!')
        else:
            db_edit(0)

    if event == '-X-':
        window['-TEXT-'].update('')
    if event == '-X0-':
        db_delete(0)
    if event == '-X1-':
        db_delete(1)
    if event == '-X2-':
        db_delete(2)
    if event == '-X3-':
        db_delete(3)
    if event == '-X4-':
        db_delete(4)
window.close()
