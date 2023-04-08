from psychopy import sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from psychopy.hardware import keyboard

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)

import os  # handy system and path functions
import sys  # to get file system encoding
import csv

from neuracle_lib.dataServer import DataServerThread
import datetime
#
#
dsi = dict(device_name='DSI-24', hostname='127.0.0.1', port=8844,
                   srate=300,
                   chanlocs=['P3', 'C3', 'F3', 'Fz', 'F4', 'C4', 'P4', 'Cz', 'CM', 'A1', 'Fp1', 'Fp2', 'T3', 'T5',
                             'O1', 'O2', 'X3', 'X2', 'F7', 'F8', 'X1', 'A2', 'T6', 'T4', 'TRG'], n_chan=25)
target_device = dsi
## 初始化 DataServerThread 线程
time_buffer = 5  # second
thread_data_server = DataServerThread(device=target_device['device_name'], n_chan=target_device['n_chan'],
                                      srate=target_device['srate'], t_buffer=time_buffer)
## 建立TCP/IP连接
notconnect = thread_data_server.connect(hostname=target_device['hostname'], port=target_device['port'])
if notconnect:
    raise TypeError("Can't connect recorder, Please open the hostport ")
else:
    # 启动线程
    thread_data_server.Daemon = True
    thread_data_server.start()
    print('Data server connected', str(datetime.datetime.now()))


def SSVEP_stimulate():

    expName = 'ssvep'  # from the Builder filename that created this script
    expInfo = {'participant': '', 'block': ''}
    dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
    if dlg.OK == False:
        thread_data_server.stop()
        core.quit()  # user pressed cancel
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    # print(_thisDir)
    filepath = _thisDir+'/data/class/'+expInfo['participant']
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    filename = filepath + '/block'+expInfo['block']


    # colour for psychopy
    WHITE = [1, 1, 1]
    BLACK = [-1, -1, -1]
    RED = [1, -1, -1]

    defaultKeyboard = keyboard.Keyboard()
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    frameTolerance = 0.001 # how close to onset before 'same' frame 起到一个近似相等的作用
    # 全屏窗口
    win = visual.Window(
        size=[2240, 1400], fullscr=True, screen=0,
        winType='pyglet', allowGUI=False, allowStencil=False,
        monitor='testMonitor', color=BLACK, colorSpace='rgb',
        blendMode='avg', useFBO=True,
        units='height')

    # Initialize components for Routine "instr"****************************
    instrClock = core.Clock()
    instrtext = visual.TextStim(win=win, name='text',
                           text='脑机接口\n\n视觉刺激实验\n\n按"空格"继续\n\n可随时按"ESC"退出',
                           font='Arial',
                           units='pix', pos=(0, 0), height=50, wrapWidth=None, ori=0,
                           color='white', colorSpace='rgb', opacity=1,
                           languageStyle='LTR',
                           depth=0.0);
    key_resp = keyboard.Keyboard()
    # 10.75-13.25 步长0.5hz
    Freq = np.array([10.25, 11.25, 12.25, 13.25, 10.75, 11.75, 12.75])
    Phas = np.array([1.05, 0.10, 0.35, 1.40, 0.45, 0.70, 1.75])




    #各刺激方块之间左右上下各间隔200px，方块大小300*300px
    mylocation = [
        [-500.0, 300.0], [0.0, 300.0], [500.0, 300.0],
        [-750.0, -200.0], [-250.0, -200], [250.0, -200.0], [750.0, -200.0]
    ]
    size_w = 300
    size_h = 300

    # Initialize components for Routine "cue"*****************************
    cueClock = core.Clock() #提示期间的时钟

    polygon_0 = visual.TextBox2(
        win=win, name='polygon_0', text='1', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_1 = visual.TextBox2(
        win=win, name='polygon_1', text='2', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_2 = visual.TextBox2(
        win=win, name='polygon_2', text='3', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_3 = visual.TextBox2(
        win=win, name='polygon_3', text='4', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_4 = visual.TextBox2(
        win=win, name='polygon_4', text='5', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_5 = visual.TextBox2(
        win=win, name='polygon_5', text='6', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)
    polygon_6 = visual.TextBox2(
        win=win, name='polygon_6', text='7', units='pix', letterHeight=200,
        pos=[0, 0], alignment='center', color=BLACK,
        fillColor=1.0, fillColorSpace='rgb',
        opacity=1)

    loop_id = -1 #当前trail

    # Initialize components for Routine "trial"**********************
    trialClock = core.Clock() #闪烁期间的时钟

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


    #实验主体部分********************************************************
    # 设置trail的次数
    trials = data.TrialHandler(nReps=7, method='random', originPath=-1,
                               trialList=[None],
                               seed=None, name='trials')
    for thisTrial in trials:
        # currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                exec('{} = thisTrial[paramName]'.format(paramName))

        # ------Prepare to start Routine "cue"------------------------------------------------------------------
        routineTimer.add(1.00000)
        # update component parameters for each repeat
        polygon_0.setPos((mylocation[0][0], mylocation[0][1]))
        polygon_0.setSize((size_w, size_h))
        polygon_1.setPos((mylocation[1][0], mylocation[1][1]))
        polygon_1.setSize((size_w, size_h))
        polygon_2.setPos((mylocation[2][0], mylocation[2][1]))
        polygon_2.setSize((size_w, size_h))
        polygon_3.setPos((mylocation[3][0], mylocation[3][1]))
        polygon_3.setSize((size_w, size_h))
        polygon_4.setPos((mylocation[4][0], mylocation[4][1]))
        polygon_4.setSize((size_w, size_h))
        polygon_5.setPos((mylocation[5][0], mylocation[5][1]))
        polygon_5.setSize((size_w, size_h))
        polygon_6.setPos((mylocation[6][0], mylocation[6][1]))
        polygon_6.setSize((size_w, size_h))

        # peiyu code cue
        selecList = [polygon_0, polygon_1, polygon_2, polygon_3, polygon_4, polygon_5, polygon_6]
        selecList[loop_id % 7].setFillColor(WHITE)  # rgb
        loop_id += 1
        selecList[loop_id % 7].setFillColor(RED)  # rgb红色提示

        # peiyu code cue End
        # keep track of which components have finished
        cueComponents = [polygon_0, polygon_1, polygon_2, polygon_3, polygon_4, polygon_5, polygon_6]
        for thisComponent in cueComponents:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        cueClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        continueRoutine = True

        # -------Run Routine "cue"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # print("***************", routineTimer.getTime())
            # while routineTimer.getTime() > 0:
            # get current time
            t = cueClock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=cueClock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *polygon_0* updates
            if polygon_0.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_0.frameNStart = frameN  # exact frame index
                polygon_0.tStart = t  # local t and not account for scr refresh
                polygon_0.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_0, 'tStartRefresh')  # time at next scr refresh
                polygon_0.setAutoDraw(True)
            if polygon_0.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_0.tStartRefresh + 1.0 - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_0.tStop = t  # not accounting for scr refresh
                    polygon_0.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_0, 'tStopRefresh')  # time at next scr refresh
                    polygon_0.setAutoDraw(False)

            # *polygon_1* updates
            if polygon_1.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_1.frameNStart = frameN  # exact frame index
                polygon_1.tStart = t  # local t and not account for scr refresh
                polygon_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_1, 'tStartRefresh')  # time at next scr refresh
                polygon_1.setAutoDraw(True)
            if polygon_1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_1.tStartRefresh + 1.0 - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_1.tStop = t  # not accounting for scr refresh
                    polygon_1.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_1, 'tStopRefresh')  # time at next scr refresh
                    polygon_1.setAutoDraw(False)

            # *polygon_2* updates
            if polygon_2.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_2.frameNStart = frameN  # exact frame index
                polygon_2.tStart = t  # local t and not account for scr refresh
                polygon_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_2, 'tStartRefresh')  # time at next scr refresh
                polygon_2.setAutoDraw(True)
            if polygon_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_2.tStartRefresh + 1.0 - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_2.tStop = t  # not accounting for scr refresh
                    polygon_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_2, 'tStopRefresh')  # time at next scr refresh
                    polygon_2.setAutoDraw(False)

            # *polygon_3* updates
            if polygon_3.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_3.frameNStart = frameN  # exact frame index
                polygon_3.tStart = t  # local t and not account for scr refresh
                polygon_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_3, 'tStartRefresh')  # time at next scr refresh
                polygon_3.setAutoDraw(True)
            if polygon_3.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_3.tStartRefresh + 1.0 - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_3.tStop = t  # not accounting for scr refresh
                    polygon_3.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_3, 'tStopRefresh')  # time at next scr refresh
                    polygon_3.setAutoDraw(False)

            # *polygon_4* updates
            if polygon_4.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_4.frameNStart = frameN  # exact frame index
                polygon_4.tStart = t  # local t and not account for scr refresh
                polygon_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_4, 'tStartRefresh')  # time at next scr refresh
                polygon_4.setAutoDraw(True)
            if polygon_4.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_4.tStartRefresh + 1.0 - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_4.tStop = t  # not accounting for scr refresh
                    polygon_4.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_4, 'tStopRefresh')  # time at next scr refresh
                    polygon_4.setAutoDraw(False)

            # *polygon_5* updates
            if polygon_5.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_5.frameNStart = frameN  # exact frame index
                polygon_5.tStart = t  # local t and not account for scr refresh
                polygon_5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_5, 'tStartRefresh')  # time at next scr refresh
                polygon_5.setAutoDraw(True)
            if polygon_5.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_5.tStartRefresh + 1.0 - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_5.tStop = t  # not accounting for scr refresh
                    polygon_5.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_5, 'tStopRefresh')  # time at next scr refresh
                    polygon_5.setAutoDraw(False)

            # *polygon_6* updates
            if polygon_6.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
                # keep track of start time/frame for later
                polygon_6.frameNStart = frameN  # exact frame index
                polygon_6.tStart = t  # local t and not account for scr refresh
                polygon_6.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(polygon_6, 'tStartRefresh')  # time at next scr refresh
                polygon_6.setAutoDraw(True)
            if polygon_6.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > polygon_6.tStartRefresh + 1.0 - frameTolerance:
                    # keep track of stop time/frame for later
                    polygon_6.tStop = t  # not accounting for scr refresh
                    polygon_6.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(polygon_6, 'tStopRefresh')  # time at next scr refresh
                    polygon_6.setAutoDraw(False)


            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                thread_data_server.stop()
                core.quit()


            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in cueComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()


        # -------Ending Routine "cue"-------
        for thisComponent in cueComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials.addData('polygon_0.started', polygon_0.tStartRefresh)

        trials.addData('polygon_0.stopped', polygon_0.tStopRefresh)
        trials.addData('polygon_1.started', polygon_1.tStartRefresh)
        trials.addData('polygon_1.stopped', polygon_1.tStopRefresh)
        trials.addData('polygon_2.started', polygon_2.tStartRefresh)
        trials.addData('polygon_2.stopped', polygon_2.tStopRefresh)
        trials.addData('polygon_3.started', polygon_3.tStartRefresh)
        trials.addData('polygon_3.stopped', polygon_3.tStopRefresh)
        trials.addData('polygon_4.started', polygon_4.tStartRefresh)
        trials.addData('polygon_4.stopped', polygon_4.tStopRefresh)
        trials.addData('polygon_5.started', polygon_5.tStartRefresh)
        trials.addData('polygon_5.stopped', polygon_5.tStopRefresh)
        trials.addData('polygon_6.started', polygon_6.tStartRefresh)
        trials.addData('polygon_6.stopped', polygon_6.tStopRefresh)

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


        # 呈现4秒的闪烁刺激
        trial_dura = 4

        seleclist2 = [polygon_trial_0, polygon_trial_1, polygon_trial_2, polygon_trial_3, polygon_trial_4, polygon_trial_5,
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

        # eegdata = thread_data_server.GetBufferData()
        # thread_data_server.ResetDataLenCount()
        # print(eegdata.shape, str(datetime.datetime.now()))
        # with open("%s.csv" % (filename), 'a', newline='') as D:
        #     mywriter = csv.writer(D, delimiter=',')
        #     mywriter.writerows(np.transpose(eegdata))
        #     # D.write(a)

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

        eegdata = thread_data_server.GetBufferData()
        print(eegdata.shape, str(datetime.datetime.now()), thread_data_server.GetDataLenCount())
        thread_data_server.ResetDataLenCount()

        with open("%s.csv" % (filename), 'a', newline='') as D:
            mywriter = csv.writer(D, delimiter=',')
            mywriter.writerows(np.transpose(eegdata))


        routineTimer.reset()




    #End----------
    thread_data_server.stop()
    win.flip()
    win.close()
    core.quit()



SSVEP_stimulate()



