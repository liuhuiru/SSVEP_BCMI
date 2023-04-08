from psychopy import gui, visual, core, data
import datetime

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, pi)
from psychopy import gui, visual, core, data
from psychopy.constants import (NOT_STARTED, STARTED, FINISHED)
from psychopy.hardware import keyboard
import os  # handy system and path functions
import sys  # to get file system encoding
import csv

from neuracle_lib.dataServer import DataServerThread

from EEGmodel.eegmodel import EEGmodel
from music.SSVEP_music.notes import play_note, ssvep_music, NoteTokenizer, play_ssvep_music





pitches = ["C4", "D4", "E4", "F4", "G4", "A4", "B4"]
dsi = dict(device_name='DSI-24', hostname='127.0.0.1', port=8844,
                   srate=300,
                   chanlocs=['P3', 'C3', 'F3', 'Fz', 'F4', 'C4', 'P4', 'Cz', 'CM', 'A1', 'Fp1', 'Fp2', 'T3', 'T5',
                             'O1', 'O2', 'X3', 'X2', 'F7', 'F8', 'X1', 'A2', 'T6', 'T4', 'TRG'], n_chan=25)
target_device = dsi
## 初始化 DataServerThread 线程
time_buffer = 1  # second
thread_data_server = DataServerThread(device=target_device['device_name'], n_chan=target_device['n_chan'],
                                      srate=target_device['srate'], t_buffer=time_buffer)
# ### 建立TCP/IP连接
notconnect = thread_data_server.connect(hostname=target_device['hostname'], port=target_device['port'])
if notconnect:
    raise TypeError("Can't connect recorder, Please open the hostport ")
else:
    # 启动线程
    thread_data_server.Daemon = True
    thread_data_server.start()
    print('Data server connected', str(datetime.datetime.now()))

def onlineSSVEP():
    expName = 'ssvep'  # from the Builder filename that created this script
    expInfo = {'participant': '', 'session': ''}
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        thread_data_server.stop()
        core.quit()  # user pressed cancel
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    # print(_thisDir)
    filepath = _thisDir + '/data/offline/' + expInfo['participant']
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + '/session' + expInfo['session']

    modelpath = './EEGmodel/model/'+expInfo['participant'] + '_model.h5'
    model = EEGmodel(modelpath)

    # colour for psychopy
    WHITE = [1, 1, 1]
    BLACK = [-1, -1, -1]
    RED = [1, -1, -1]
    GREEN = [-1, 0, -1]

    defaultKeyboard = keyboard.Keyboard()
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    frameTolerance = 0.001  # how close to onset before 'same' frame 起到一个近似相等的作用

    # noteList = [1, 2, 3, 4, 5, 6, 7]
    # noteList = [5, 3, 5, 3, 5, 3, 1, 2, 4, 3, 2, 5]
    # noteList = [5, 3, 5, 3, 5, 3, 1]
    noteList = [5, 3, 5, 3, 5, 3, 1, 2, 4, 3, 2, 5,
     5, 3, 5, 3, 5, 3, 1, 2, 4, 3, 2, 1,
     2, 2, 4, 4, 3, 1, 5, 2, 4, 3, 2, 5,
     5, 3, 5, 3, 5, 3, 1, 2, 4, 3, 2, 1]
    outputNoteList = []

    # 全屏窗口
    win = visual.Window(
        size=[2240, 1400], fullscr=True, screen=0,
        # size=[500, 500], fullscr=False, screen=0,
        winType='pyglet', allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=BLACK, colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='height')

    # Initialize components for Routine "instr"****************************
    instrClock = core.Clock()
    instrtext = visual.TextStim(win=win, name='text',
                                text='SSVEP脑机音乐接口系统\n\n自由作曲模式\n\n请在闪烁期间注视希望输入的音符\n\n一次可连续输入5个音符\n\n最多输入十次\n\n按"空格"继续\n\n可随时按"ESC"退出',
                                font='Arial',
                                units='pix', pos=(0, 0), height=50, wrapWidth=None, ori=0,
                                color='white', colorSpace='rgb', opacity=1,
                                languageStyle='LTR',
                                depth=0.0);
    key_resp = keyboard.Keyboard()
    # 10.75-13.25 步长0.5hz
    Freq = np.array([10.25, 11.25, 12.25, 13.25, 10.75, 11.75, 12.75])
    Phas = np.array([1.05, 0.10, 0.35, 1.40, 0.45, 0.70, 1.75])

    # 各刺激方块之间左右上下各间隔200px，方块大小300*300px
    mylocation = [
        [-500.0, 300.0], [0.0, 300.0], [500.0, 300.0],
        [-750.0, -200.0], [-250.0, -200], [250.0, -200.0], [750.0, -200.0]
    ]
    size_w = 300
    size_h = 300

    # Initialize components for Routine "cue"*****************************
    cueClock = core.Clock()  # 提示期间的时钟

    output_text = visual.TextStim(win=win, name='text',
                                 text='输出序列：',
                                 font='Arial',
                                 units='pix', pos=(0, 0), height=50, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=0.0);
    output_note_text = "";
    output_note = visual.TextStim(win=win, name='text',
                                 text=output_note_text,
                                 font='Arial',
                                 anchorHoriz="left",
                                  alignText="left",
                                 units='pix', pos=(0, 0), height=50, wrapWidth=None, ori=0,
                                 color='white', colorSpace='rgb', opacity=1,
                                 languageStyle='LTR',
                                 depth=0.0);

    musicClock = core.Clock()
    wait_music_text = visual.TextStim(win=win, name='text',
                                      text='您的SSVEP输入旋律简谱为:\n\n' + output_note_text +
                                           '\n\n音乐正在生成中\n\n请耐心等待......',
                                      font='Arial',
                                      anchorHoriz="center",
                                      alignText="center",
                                      units='pix', pos=(0, 0), height=50, wrapWidth=None, ori=0,
                                      color='white', colorSpace='rgb', opacity=1,
                                      languageStyle='LTR',
                                      depth=0.0);
    play_music_text = visual.TextStim(win=win, name='text',
                                      text='当前正在播放由AI为您合成的音乐',
                                      font='Arial',
                                      anchorHoriz="center",
                                      alignText="center",
                                      units='pix', pos=(0, 0), height=50, wrapWidth=None, ori=0,
                                      color='white', colorSpace='rgb', opacity=1,
                                      languageStyle='LTR',
                                      depth=0.0);
    end_music_text = visual.TextStim(win=win, name='text',
                                     text='播放结束\n\n按空格键继续输入音符\n\n按ESC键退出系统',
                                     font='Arial',
                                     anchorHoriz="center",
                                     alignText="center",
                                     units='pix', pos=(0, 0), height=50, wrapWidth=None, ori=0,
                                     color='white', colorSpace='rgb', opacity=1,
                                     languageStyle='LTR',
                                     depth=0.0);

    loop_id = 0  # 当前trail

    # Initialize components for Routine "trial"**********************
    trialClock = core.Clock()  # 闪烁期间的时钟

    polygon_trial_0 = visual.TextBox2(
        win=win, name='polygon_trial_0', text='1', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_trial_1 = visual.TextBox2(
        win=win, name='polygon_trial_1', text='2', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_trial_2 = visual.TextBox2(
        win=win, name='polygon_trial_2', text='3', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_trial_3 = visual.TextBox2(
        win=win, name='polygon_trial_3', text='4', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_trial_4 = visual.TextBox2(
        win=win, name='polygon_trial_4', text='5', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_trial_5 = visual.TextBox2(
        win=win, name='polygon_trial_5', text='6', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_trial_6 = visual.TextBox2(
        win=win, name='polygon_trial_6', text='7', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)

    # Initialize components for Routine "feedback"**********************
    fbClock = core.Clock()  # 反馈期间的时钟

    polygon_feedback_0 = visual.TextBox2(
        win=win, name='polygon_feedback_0', text='1', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_feedback_1 = visual.TextBox2(
        win=win, name='polygon_feedback_1', text='2', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_feedback_2 = visual.TextBox2(
        win=win, name='polygon_feedback_2', text='3', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_feedback_3 = visual.TextBox2(
        win=win, name='polygon_feedback_3', text='4', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_feedback_4 = visual.TextBox2(
        win=win, name='polygon_feedback_4', text='5', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_feedback_5 = visual.TextBox2(
        win=win, name='polygon_feedback_5', text='6', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_feedback_6 = visual.TextBox2(
        win=win, name='polygon_feedback_6', text='7', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)

    feedback_loop_id = 0



    routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 从上次reset的时间开始倒计时

    # ------Prepare to start Routine "instr"----------------------------------------------------------
    # update component parameters for each repeat
    key_resp.keys = []
    key_resp.rt = []
    # keep track of which components have finished
    instrComponents = [instrtext, key_resp]
    for thisComponent in instrComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    instrClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    continueRoutine = True

    # -------Run Routine "instr"--------------------------------
    while continueRoutine:
        # get current time
        t = instrClock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=instrClock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *text* updates
        if instrtext.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            instrtext.frameNStart = frameN  # exact frame index
            instrtext.tStart = t  # local t and not account for scr refresh
            instrtext.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instrtext, 'tStartRefresh')  # time at next scr refresh
            instrtext.setAutoDraw(True)

        # *key_resp* updates
        waitOnFlip = False
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            key_resp.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
            if len(theseKeys):
                theseKeys = theseKeys[0]  # at least one key was pressed

                # check for quit:
                if "escape" == theseKeys:
                    endExpNow = True
                # a response ends the routine
                continueRoutine = False

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            thread_data_server.stop()
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in instrComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "instr"-------
    for thisComponent in instrComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # thisExp.addData('text.started', text.tStartRefresh)
    # thisExp.addData('text.stopped', text.tStopRefresh)
    # the Routine "instr" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # 实验主体部分********************************************************
    output_text.setPos((-900.0, 620.0))
    output_note.setPos((-800, 620))

    if output_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        output_text.frameNStart = frameN  # exact frame index
        output_text.tStart = t  # local t and not account for scr refresh
        output_text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(output_text, 'tStartRefresh')  # time at next scr refresh
        output_text.setAutoDraw(True)
    if output_note.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        output_note.frameNStart = frameN  # exact frame index
        output_note.tStart = t  # local t and not account for scr refresh
        output_note.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(output_note, 'tStartRefresh')  # time at next scr refresh
        output_note.setAutoDraw(True)



    # 设置trail的次数
    trials = data.TrialHandler(nReps=50, method='random', originPath=-1,
                               trialList=[None],
                               seed=None, name='trials')
    for thisTrial in trials:
        # currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))


        # ------Prepare to start Routine "trial"-----------------------------------------------------------------------
        # update component parameters for each repeat
        polygon_trial_0.setPos((mylocation[0][0], mylocation[0][1]))
        polygon_trial_0.setSize((size_w, size_h))
        polygon_trial_1.setPos((mylocation[1][0], mylocation[1][1]))
        polygon_trial_1.setSize((size_w, size_h))
        polygon_trial_2.setPos((mylocation[2][0], mylocation[2][1]))
        polygon_trial_2.setSize((size_w, size_h))
        polygon_trial_3.setPos((mylocation[3][0], mylocation[3][1]))
        polygon_trial_3.setSize((size_w, size_h))
        polygon_trial_4.setPos((mylocation[4][0], mylocation[4][1]))
        polygon_trial_4.setSize((size_w, size_h))
        polygon_trial_5.setPos((mylocation[5][0], mylocation[5][1]))
        polygon_trial_5.setSize((size_w, size_h))
        polygon_trial_6.setPos((mylocation[6][0], mylocation[6][1]))
        polygon_trial_6.setSize((size_w, size_h))

        # 呈现2秒的闪烁刺激,方便用户进行视线转移
        trial_dura = 2
        # thread_data_server.ResetDataLenCount()

        seleclist2 = [polygon_trial_0, polygon_trial_1, polygon_trial_2, polygon_trial_3, polygon_trial_4,
                      polygon_trial_5,
                      polygon_trial_6]
        # keep track of which components have finished
        trialComponents = [polygon_trial_0, polygon_trial_1, polygon_trial_2, polygon_trial_3, polygon_trial_4,
                           polygon_trial_5, polygon_trial_6]
        for thisComponent in trialComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        trialClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True
        print('闪烁开始, loop_id:', loop_id, str(datetime.datetime.now()))

        # buffer清零******************************************
        # thread_data_server.resetBuffer()

        # -------Run Routine "trial"-------
        while continueRoutine:
            # get current time
            t = trialClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=trialClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *polygon_trial_0* updates

            if polygon_trial_0.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_trial_0.frameNStart = frameN  # exact frame index
                polygon_trial_0.tStart = t  # local t and not account for scr refresh
                polygon_trial_0.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_trial_0, 'tStartRefresh')  # time at next scr refresh
                polygon_trial_0.setAutoDraw(True)
            if polygon_trial_0.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_trial_0.tStartRefresh + trial_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_trial_0.tStop = t  # not accounting for scr refresh
                    polygon_trial_0.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_trial_0, 'tStopRefresh')  # time at next scr refresh
                    polygon_trial_0.setAutoDraw(False)
            if polygon_trial_0.status == STARTED:  # only update if drawing
                polygon_trial_0.setFillColor([1, 1, 1], log=False)

            # *polygon_trial_1* updates
            if polygon_trial_1.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_trial_1.frameNStart = frameN  # exact frame index
                polygon_trial_1.tStart = t  # local t and not account for scr refresh
                polygon_trial_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_trial_1, 'tStartRefresh')  # time at next scr refresh
                polygon_trial_1.setAutoDraw(True)
            if polygon_trial_1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_trial_1.tStartRefresh + trial_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_trial_1.tStop = t  # not accounting for scr refresh
                    polygon_trial_1.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_trial_1, 'tStopRefresh')  # time at next scr refresh
                    polygon_trial_1.setAutoDraw(False)
            if polygon_trial_1.status == STARTED:  # only update if drawing
                polygon_trial_1.setFillColor([1, 1, 1], log=False)

            # *polygon_trial_2* updates
            if polygon_trial_2.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_trial_2.frameNStart = frameN  # exact frame index
                polygon_trial_2.tStart = t  # local t and not account for scr refresh
                polygon_trial_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_trial_2, 'tStartRefresh')  # time at next scr refresh
                polygon_trial_2.setAutoDraw(True)
            if polygon_trial_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_trial_2.tStartRefresh + trial_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_trial_2.tStop = t  # not accounting for scr refresh
                    polygon_trial_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_trial_2, 'tStopRefresh')  # time at next scr refresh
                    polygon_trial_2.setAutoDraw(False)
            if polygon_trial_2.status == STARTED:  # only update if drawing
                polygon_trial_2.setFillColor([1, 1, 1], log=False)

            # *polygon_trial_3* updates
            if polygon_trial_3.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_trial_3.frameNStart = frameN  # exact frame index
                polygon_trial_3.tStart = t  # local t and not account for scr refresh
                polygon_trial_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_trial_3, 'tStartRefresh')  # time at next scr refresh
                polygon_trial_3.setAutoDraw(True)
            if polygon_trial_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_trial_3.tStartRefresh + trial_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_trial_3.tStop = t  # not accounting for scr refresh
                    polygon_trial_3.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_trial_3, 'tStopRefresh')  # time at next scr refresh
                    polygon_trial_3.setAutoDraw(False)
            if polygon_trial_3.status == STARTED:  # only update if drawing
                polygon_trial_3.setFillColor([1, 1, 1], log=False)

            # # *polygon_trial_4* updates
            if polygon_trial_4.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_trial_4.frameNStart = frameN  # exact frame index
                polygon_trial_4.tStart = t  # local t and not account for scr refresh
                polygon_trial_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_trial_4, 'tStartRefresh')  # time at next scr refresh
                polygon_trial_4.setAutoDraw(True)
            if polygon_trial_4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_trial_4.tStartRefresh + trial_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_trial_4.tStop = t  # not accounting for scr refresh
                    polygon_trial_4.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_trial_4, 'tStopRefresh')  # time at next scr refresh
                    polygon_trial_4.setAutoDraw(False)

            # *polygon_trial_5* updates
            if polygon_trial_5.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_trial_5.frameNStart = frameN  # exact frame index
                polygon_trial_5.tStart = t  # local t and not account for scr refresh
                polygon_trial_5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_trial_5, 'tStartRefresh')  # time at next scr refresh
                polygon_trial_5.setAutoDraw(True)
            if polygon_trial_5.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_trial_5.tStartRefresh + trial_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_trial_5.tStop = t  # not accounting for scr refresh
                    polygon_trial_5.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_trial_5, 'tStopRefresh')  # time at next scr refresh
                    polygon_trial_5.setAutoDraw(False)
            if polygon_trial_5.status == STARTED:  # only update if drawing
                polygon_trial_5.setFillColor([1, 1, 1], log=False)

            # *polygon_trial_6* updates
            if polygon_trial_6.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_trial_6.frameNStart = frameN  # exact frame index
                polygon_trial_6.tStart = t  # local t and not account for scr refresh
                polygon_trial_6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_trial_6, 'tStartRefresh')  # time at next scr refresh
                polygon_trial_6.setAutoDraw(True)
            if polygon_trial_6.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_trial_6.tStartRefresh + trial_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_trial_6.tStop = t  # not accounting for scr refresh
                    polygon_trial_6.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_trial_6, 'tStopRefresh')  # time at next scr refresh
                    polygon_trial_6.setAutoDraw(False)
            if polygon_trial_6.status == STARTED:  # only update if drawing
                polygon_trial_6.setFillColor([1, 1, 1], log=False)

            # peiyu code
            Amp = (sin(2 * pi * Freq * frameN / 60 + Phas) - 0.5) * 2

            # 控制方块按规定的频率闪烁
            for idx in range(7):
                seleclist2[idx].setFillColor([Amp[idx]])
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                thread_data_server.stop()
                core.quit()

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()


        # -------Ending Routine "trial"-------
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('polygon_trial_0.started', polygon_trial_0.tStartRefresh)
        trials.addData('polygon_trial_0.stopped', polygon_trial_0.tStopRefresh)
        trials.addData('polygon_trial_1.started', polygon_trial_1.tStartRefresh)
        trials.addData('polygon_trial_1.stopped', polygon_trial_1.tStopRefresh)
        trials.addData('polygon_trial_2.started', polygon_trial_2.tStartRefresh)
        trials.addData('polygon_trial_2.stopped', polygon_trial_2.tStopRefresh)
        trials.addData('polygon_trial_3.started', polygon_trial_3.tStartRefresh)
        trials.addData('polygon_trial_3.stopped', polygon_trial_3.tStopRefresh)
        trials.addData('polygon_trial_4.started', polygon_trial_4.tStartRefresh)
        trials.addData('polygon_trial_4.stopped', polygon_trial_4.tStopRefresh)
        trials.addData('polygon_trial_5.started', polygon_trial_5.tStartRefresh)
        trials.addData('polygon_trial_5.stopped', polygon_trial_5.tStopRefresh)
        trials.addData('polygon_trial_6.started', polygon_trial_6.tStartRefresh)
        trials.addData('polygon_trial_6.stopped', polygon_trial_6.tStopRefresh)
        # the Routine "trial" was not non-slip safe, so reset the non-slip timer

        print('闪烁结束, loop_id:', loop_id, str(datetime.datetime.now()))


        eegdata = thread_data_server.GetBufferData()
        print(eegdata.shape, str(datetime.datetime.now()), thread_data_server.GetDataLenCount())
        # # with open("%s.csv" % (filename), 'a', newline='') as D:
        # #     mywriter = csv.writer(D, delimiter=',')
        # #     mywriter.writerows(np.transpose(eegdata[:, 900:]))
        #
        pred = model.predict(eegdata)
        # pred = noteList[loop_id] - 1
        # thread_data_server.ResetDataLenCount()


        print('******pred', pred)
        outputNoteList.append(pred + 1)

        output_note_text += str(pred+1)
        output_note.setText(output_note_text)

        loop_id += 1


        routineTimer.reset()
        # ------Prepare to start Routine "feedback"-----------------------------------------------------------------------
        routineTimer.add(1)
        # update component parameters for each repeat
        polygon_feedback_0.setPos((mylocation[0][0], mylocation[0][1]))
        polygon_feedback_0.setSize((size_w, size_h))
        polygon_feedback_1.setPos((mylocation[1][0], mylocation[1][1]))
        polygon_feedback_1.setSize((size_w, size_h))
        polygon_feedback_2.setPos((mylocation[2][0], mylocation[2][1]))
        polygon_feedback_2.setSize((size_w, size_h))
        polygon_feedback_3.setPos((mylocation[3][0], mylocation[3][1]))
        polygon_feedback_3.setSize((size_w, size_h))
        polygon_feedback_4.setPos((mylocation[4][0], mylocation[4][1]))
        polygon_feedback_4.setSize((size_w, size_h))
        polygon_feedback_5.setPos((mylocation[5][0], mylocation[5][1]))
        polygon_feedback_5.setSize((size_w, size_h))
        polygon_feedback_6.setPos((mylocation[6][0], mylocation[6][1]))
        polygon_feedback_6.setSize((size_w, size_h))

        # peiyu code cue
        selecList3 = [polygon_feedback_0, polygon_feedback_1, polygon_feedback_2, polygon_feedback_3, polygon_feedback_4, polygon_feedback_5, polygon_feedback_6]
        for idx in range(7):
            selecList3[idx].setFillColor(WHITE)
         # rgb
        feedback_loop_id += 1
        selecList3[pred].setFillColor(GREEN)  # 绿色反馈信号
        fbComponents = [polygon_feedback_0, polygon_feedback_1, polygon_feedback_2, polygon_feedback_3, polygon_feedback_4, polygon_feedback_5, polygon_feedback_6]
        for thisComponent in fbComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        fbClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True

        fb_dura = 0.1



        # -------Run Routine "feedback"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # print("***************", routineTimer.getTime())
            # while routineTimer.getTime() > 0:
            # get current time
            t = fbClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=fbClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *polygon_feedback_0* updates
            if polygon_feedback_0.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_feedback_0.frameNStart = frameN  # exact frame index
                polygon_feedback_0.tStart = t  # local t and not account for scr refresh
                polygon_feedback_0.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_feedback_0, 'tStartRefresh')  # time at next scr refresh
                polygon_feedback_0.setAutoDraw(True)
            if polygon_feedback_0.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_feedback_0.tStartRefresh + fb_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_feedback_0.tStop = t  # not accounting for scr refresh
                    polygon_feedback_0.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_feedback_0, 'tStopRefresh')  # time at next scr refresh
                    polygon_feedback_0.setAutoDraw(False)

            # *polygon_feedback_1* updates
            if polygon_feedback_1.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_feedback_1.frameNStart = frameN  # exact frame index
                polygon_feedback_1.tStart = t  # local t and not account for scr refresh
                polygon_feedback_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_feedback_1, 'tStartRefresh')  # time at next scr refresh
                polygon_feedback_1.setAutoDraw(True)
            if polygon_feedback_1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_feedback_1.tStartRefresh + fb_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_feedback_1.tStop = t  # not accounting for scr refresh
                    polygon_feedback_1.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_feedback_1, 'tStopRefresh')  # time at next scr refresh
                    polygon_feedback_1.setAutoDraw(False)

            # *polygon_feedback_2* updates
            if polygon_feedback_2.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_feedback_2.frameNStart = frameN  # exact frame index
                polygon_feedback_2.tStart = t  # local t and not account for scr refresh
                polygon_feedback_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_feedback_2, 'tStartRefresh')  # time at next scr refresh
                polygon_feedback_2.setAutoDraw(True)
            if polygon_feedback_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_feedback_2.tStartRefresh + fb_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_feedback_2.tStop = t  # not accounting for scr refresh
                    polygon_feedback_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_feedback_2, 'tStopRefresh')  # time at next scr refresh
                    polygon_feedback_2.setAutoDraw(False)

            # *polygon_feedback_3* updates
            if polygon_feedback_3.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_feedback_3.frameNStart = frameN  # exact frame index
                polygon_feedback_3.tStart = t  # local t and not account for scr refresh
                polygon_feedback_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_feedback_3, 'tStartRefresh')  # time at next scr refresh
                polygon_feedback_3.setAutoDraw(True)
            if polygon_feedback_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_feedback_3.tStartRefresh + fb_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_feedback_3.tStop = t  # not accounting for scr refresh
                    polygon_feedback_3.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_feedback_3, 'tStopRefresh')  # time at next scr refresh
                    polygon_feedback_3.setAutoDraw(False)

            # *polygon_4* updates
            if polygon_feedback_4.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_feedback_4.frameNStart = frameN  # exact frame index
                polygon_feedback_4.tStart = t  # local t and not account for scr refresh
                polygon_feedback_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_feedback_4, 'tStartRefresh')  # time at next scr refresh
                polygon_feedback_4.setAutoDraw(True)
            if polygon_feedback_4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_feedback_4.tStartRefresh + fb_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_feedback_4.tStop = t  # not accounting for scr refresh
                    polygon_feedback_4.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_feedback_4, 'tStopRefresh')  # time at next scr refresh
                    polygon_feedback_4.setAutoDraw(False)

            # *polygon_feedback_5* updates
            if polygon_feedback_5.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_feedback_5.frameNStart = frameN  # exact frame index
                polygon_feedback_5.tStart = t  # local t and not account for scr refresh
                polygon_feedback_5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_feedback_5, 'tStartRefresh')  # time at next scr refresh
                polygon_feedback_5.setAutoDraw(True)
            if polygon_feedback_5.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_feedback_5.tStartRefresh + fb_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_feedback_5.tStop = t  # not accounting for scr refresh
                    polygon_feedback_5.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_feedback_5, 'tStopRefresh')  # time at next scr refresh
                    polygon_feedback_5.setAutoDraw(False)

            # *polygon_feedback_6* updates
            if polygon_feedback_6.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_feedback_6.frameNStart = frameN  # exact frame index
                polygon_feedback_6.tStart = t  # local t and not account for scr refresh
                polygon_feedback_6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_feedback_6, 'tStartRefresh')  # time at next scr refresh
                polygon_feedback_6.setAutoDraw(True)
            if polygon_feedback_6.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_feedback_6.tStartRefresh + fb_dura - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_feedback_6.tStop = t  # not accounting for scr refresh
                    polygon_feedback_6.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_feedback_6, 'tStopRefresh')  # time at next scr refresh
                    polygon_feedback_6.setAutoDraw(False)

            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                thread_data_server.stop()
                core.quit()

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in fbComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen routineTimer.getTime() > 0

            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
                play_note(pitch=pitches[pred])

        # print(1, str(datetime.datetime.now()))
        # play_note(pitch=pitches[loop_id % 7])
        # print(2, str(datetime.datetime.now()))
        # -------Ending Routine "feedback"-------
        for thisComponent in fbComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('polygon_feedback_0.started', polygon_feedback_0.tStartRefresh)
        trials.addData('polygon_feedback_0.stopped', polygon_feedback_0.tStopRefresh)
        trials.addData('polygon_feedback_1.started', polygon_feedback_1.tStartRefresh)
        trials.addData('polygon_feedback_1.stopped', polygon_feedback_1.tStopRefresh)
        trials.addData('polygon_feedback_2.started', polygon_feedback_2.tStartRefresh)
        trials.addData('polygon_feedback_2.stopped', polygon_feedback_2.tStopRefresh)
        trials.addData('polygon_feedback_3.started', polygon_feedback_3.tStartRefresh)
        trials.addData('polygon_feedback_3.stopped', polygon_feedback_3.tStopRefresh)
        trials.addData('polygon_feedback_4.started', polygon_feedback_4.tStartRefresh)
        trials.addData('polygon_feedback_4.stopped', polygon_feedback_4.tStopRefresh)
        trials.addData('polygon_feedback_5.started', polygon_feedback_5.tStartRefresh)
        trials.addData('polygon_feedback_5.stopped', polygon_feedback_5.tStopRefresh)
        trials.addData('polygon_feedback_6.started', polygon_feedback_6.tStartRefresh)
        trials.addData('polygon_feedback_6.stopped', polygon_feedback_6.tStopRefresh)

        routineTimer.reset()

        # AI music ******************************************************************
        if(loop_id % 5 == 0):
            print(outputNoteList)
            output_text.setAutoDraw(False)
            output_note.setAutoDraw(False)
            win.flip()
            wait_music_text.setText('您的SSVEP输入旋律简谱为:\n\n' + output_note_text +
                                           '\n\n音乐正在生成中\n\n请耐心等待......')
            continueRoutine = True
            musicComponents = [wait_music_text, play_music_text, end_music_text]
            for thisComponent in musicComponents:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
                    # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            musicClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
            frameN = -1

            if wait_music_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                wait_music_text.frameNStart = frameN  # exact frame index
                wait_music_text.tStart = t  # local t and not account for scr refresh
                wait_music_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(wait_music_text, 'tStartRefresh')  # time at next scr refresh
                wait_music_text.setAutoDraw(True)
            win.flip()

            # 生成AI音乐
            ssvep_music(outputNoteList, 100, expInfo)
            wait_music_text.setAutoDraw(False)

            if play_music_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                play_music_text.frameNStart = frameN  # exact frame index
                play_music_text.tStart = t  # local t and not account for scr refresh
                play_music_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(play_music_text, 'tStartRefresh')  # time at next scr refresh
                play_music_text.setAutoDraw(True)
            win.flip()
            play_ssvep_music(expInfo)
            play_music_text.setAutoDraw(False)
            while continueRoutine:
                t = musicClock.getTime()
                tThisFlip = win.getFutureFlipTime(clock=musicClock)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)

                if end_music_text.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                    # keep track of start time/frame for later
                    end_music_text.frameNStart = frameN  # exact frame index
                    end_music_text.tStart = t  # local t and not account for scr refresh
                    end_music_text.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(end_music_text, 'tStartRefresh')  # time at next scr refresh
                    end_music_text.setAutoDraw(True)

                if not continueRoutine:
                    break

                if defaultKeyboard.getKeys(keyList=["escape"]):
                    thread_data_server.stop()
                    core.quit()
                if continueRoutine:
                    win.flip()
                if defaultKeyboard.getKeys(keyList=["space"]):
                    continueRoutine = False

            end_music_text.setAutoDraw(False)
            output_note.setAutoDraw(True)
            output_text.setAutoDraw(True)





    # End----------
    thread_data_server.stop()
    win.flip()
    win.close()
    core.quit()



onlineSSVEP()