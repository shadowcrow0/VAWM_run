#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.1.1),
    on August 13, 2026, at 10:13
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

── GRTv3_ada.py ─────────────────────────────────────────────────────────────
Successor of GRTv3_a.py: both dimensions (colour arc ±24 dE00 around anchor 303°, reported as blue / pink; SNR ±18 dB on a single /bi/ token, reported as [bi] / [pi]) are calibrated per participant by two independent Psi procedures (AGRT) using the full working-memory task — block 1 calibrates colour, block 2 sound (all valid trials, correct option framed after each answer), then N_PRACTICE practice trials and the main task.
"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (
    NOT_STARTED, STARTED, PLAYING, PAUSED, STOPPED, STOPPING, FINISHED, PRESSED, 
    RELEASED, FOREVER, priority
)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

# Audio output device: handled by audio_pick.py (list devices, open for real, prefer headphones).
# On a new machine run `python audio_pick.py` first. Name the device with --audio-device "NAME",
# the environment variable VAWM_AUDIO_DEVICE, or `python audio_pick.py --set "NAME"`.
# --require-headphones stops instead of falling back to speakers; --list-audio only prints the devices.
from audio_pick import setup_from_argv
AUDIO = setup_from_argv(sys.argv, require_headphones=True)   # GRT: SNR task, no headphones = no run

from psychopy.hardware.button import ButtonBox

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.1.1'
expName = 'GRTv3_ada'
expVersion = ''
# a list of functions to run when the experiment ends (starts off blank)
runAtExit = []
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'expVersion|hid': expVersion,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = (1024, 768)
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']
    # replace default participant ID
    if prefs.piloting['replaceParticipantID']:
        expInfo['participant'] = 'pilot'

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version=expVersion,
        extraInfo=expInfo, runtimeInfo=None,
        originPath='C:\\Users\\spt904\\OneDrive - University of Texas at San Antonio\\Desktop\\Visual_AudioWM-main\\GRTv2.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    # store pilot mode in data file
    thisExp.addData('piloting', PILOTING, priority=priority.LOW)
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='deg',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'deg'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    if PILOTING:
        # show a visual indicator if we're in piloting mode
        if prefs.piloting['showPilotingIndicator']:
            win.showPilotingIndicator()
        # always show the mouse in piloting mode
        if prefs.piloting['forceMouseVisible']:
            win.mouseVisible = True
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    ioSession = ioServer = eyetracker = None
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ptb'
        )
    from audio_pick import register_label
    register_label(AUDIO['name'], label='Laptop')   # the psyexp deviceLabel is unchanged
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], currentRoutine=None):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    currentRoutine : psychopy.data.Routine
        Current Routine we are in at time of pausing, if any. This object tells PsychoPy what Components to pause/play/dispatch.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='PsychToolbox',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # dispatch messages on response components
        if currentRoutine is not None:
            for comp in currentRoutine.getDispatchComponents():
                comp.device.dispatchMessages()
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    if currentRoutine is not None:
        for comp in currentRoutine.getPlaybackComponents():
            comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # update experiment info
    expInfo['date'] = data.getDateStr()
    expInfo['expName'] = expName
    expInfo['expVersion'] = expVersion
    expInfo['psychopyVersion'] = psychopyVersion
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='PsychToolbox'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Intro" ---
    # Run 'Begin Experiment' code from check_screen
    from psychopy import monitors
    m = win.monitor
    print(f"monitor: {m.name}")
    print(f"width_cm: {m.getWidth()}, dist_cm: {m.getDistance()}")
    print(f"res: {m.getSizePix()}, win: {win.size}")
    text = visual.TextStim(win=win, name='text',
        text='Welcome, and thank you for taking part.\n\nThis session has two parts: a short calibration, then the main experiment. Please make sure you are wearing the headphones before continuing.\n\nPress the space bar to continue.',
        font='Arial',
        pos=(0, 0), draggable=False, height=1.0, wrapWidth=24, ori=0.0,
        color='white', colorSpace='rgb', opacity=None,
        languageStyle='LTR', alignText='left', anchorHoriz='center',
        depth=-1.0);
    key_resp = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "instruction_normal" ---
    instruction_normal_text = visual.TextStim(win=win, name='instruction_normal_text',
        text='The task.\n\nFour coloured squares will appear one at a time, one in each corner of the screen, and each of them comes with its own speech sound. Try to remember which colour and which sound belong together and where they appeared.\n\nA frame will then appear at one of the corners, and an item will appear in it. When you see the frame, recall what has just appeared. On the final screen four options are shown, one in each corner - Each option is a colour with a syllable label, [bi] or [pi], underneath - choose the one you have in mind by pressing the key for its position:\n\n        i = upper left            o = upper right\n        k = lower left            l = lower right\n\nThe picture below shows how the four keys point to the four corners.\n\nThe session has four parts: colour calibration, sound calibration, a short practice, then the main experiment in four blocks with a rest after each one. During calibration and practice the correct option is framed after each answer. The colours and sounds are adjusted to stay difficult, so feeling unsure is normal - just give your best guess every time. Answer as accurately as you can - speed is not important.\n\nPress the space bar to begin.',
        font='Arial',
        pos=(0, 3.0), draggable=False, height=0.65, wrapWidth=26, ori=0.0,
        color='white', colorSpace='rgb', opacity=None,
        languageStyle='LTR', alignText='left', anchorHoriz='center',
        depth=0.0);
    instruction_key_img = visual.ImageStim(
        win=win, name='instruction_key_img',
        image='stimuli/box_keys_iokl.png', mask=None, anchor='center',
        ori=0.0, pos=(0, -7.0), size=(5.5, 5.0),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    instruction_normal_key = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "study" ---
    # Run 'Begin Experiment' code from pattern
    from psychopy import monitors
    import numpy as np
    rng = np.random.default_rng()
    
    # --------------------------------------------------------------------
    #   itemColhex = [C1, C2, C1, C2]  ->  i & 1
    #   itemAudi   = [S1, S1, S2, S2]  ->  i >> 1
    #
    # --------------------------------------------------------------------
    REL_NAME = {0: 'valid', 1: 'colour_only', 2: 'sound_only', 3: 'both'}
    
    N_VALID_PER_CELL   = 24
    N_INVALID_PER_CELL = 4
    BLOCK_SIZE         = 144
    
    strata = []
    for _it in range(4):
        for _sp in range(4):
            strata.append(((1, _it, 0, _sp), N_VALID_PER_CELL))
            for _rel in (1, 2, 3):
                strata.append(((0, _it, _rel, _sp), N_INVALID_PER_CELL))
    
    N_MAIN   = sum(n for _, n in strata)
    n_blocks = N_MAIN // BLOCK_SIZE
    blocks   = [[] for _ in range(n_blocks)]
    _k = 0
    for _cond, _n in strata:
        for _ in range(_n):
            blocks[_k % n_blocks].append(_cond)
            _k += 1
    for _bi in range(n_blocks):
        blocks[_bi] = [blocks[_bi][i] for i in rng.permutation(len(blocks[_bi]))]
    main_plan = [t for b in blocks for t in b]
    
    N_ADAPT_COL = 72
    N_ADAPT_SND = 72
    N_ADAPT     = N_ADAPT_COL + N_ADAPT_SND
    def _adapt_plan(n):
        _sp = [i % 4 for i in range(n)]
        return [(1, None, 0, int(_sp[i])) for i in rng.permutation(n)]
    adapt_plan = _adapt_plan(N_ADAPT_COL) + _adapt_plan(N_ADAPT_SND)

    N_PRACTICE        = 15
    FEEDBACK_PRE_MAIN = True
    FEEDBACK_SEC      = 1.5
    _n_valid   = round(N_PRACTICE * 2 / 3)      # 10 valid
    _n_invalid = N_PRACTICE - _n_valid          # 5 invalid
    _valid_pool = [(1, _it, 0, _sp) for _it in range(4) for _sp in range(4)]
    _inval_pool = [(0, _it, _rel, _sp) for _it in range(4) for _rel in (1, 2, 3) for _sp in range(4)]
    practice_plan = ([_valid_pool[i] for i in rng.permutation(len(_valid_pool))[:_n_valid]] +
                     [_inval_pool[i] for i in rng.permutation(len(_inval_pool))[:_n_invalid]])
    practice_plan = [practice_plan[i] for i in rng.permutation(len(practice_plan))]
    
    trial_plan = adapt_plan + practice_plan + main_plan
    N_PRE      = N_ADAPT + N_PRACTICE
    N_TRIALS   = len(trial_plan)
    trial_i    = -1
    practice_correct = 0
    
    print(f"[plan] calibration colour {N_ADAPT_COL} + sound {N_ADAPT_SND} + practice {N_PRACTICE}"
          f"(all with feedback) + main {N_MAIN} = {N_TRIALS} trials;"
          f" main {n_blocks} blocks x {BLOCK_SIZE}")
    
    import json
    with open('agrt_colour_lut.json', encoding='utf-8') as _f:
        _LUT = json.load(_f)
    _LUT_HEX = _LUT['hex']
    _LUT_ARC = _LUT['arc_min'] + np.arange(len(_LUT_HEX)) * _LUT['step']
    
    def colour_for(arc):
        """Arc-length coordinate (dE00) -> '#RRGGBB'; raises outside the usable range instead of clipping silently."""
        if not (_LUT_ARC[0] <= arc <= _LUT_ARC[-1]):
            raise ValueError(f"colour arc length {arc} is outside the usable range "
                             f"[{_LUT_ARC[0]:.2f}, {_LUT_ARC[-1]:.2f}] dE00")
        return _LUT_HEX[int(np.abs(_LUT_ARC - arc).argmin())]
    
    COLOUR_ARC = [-3.0, +3.0]
    COLOUR_HEX = [colour_for(a) for a in COLOUR_ARC]
    print(f"[colour] anchor h={_LUT['anchor_h']} L*={_LUT['lstar']} C*={_LUT['cstar']};"
          f" arc {COLOUR_ARC} -> {COLOUR_HEX}")
    
    Fixation = visual.ShapeStim(
        win=win, name='Fixation', vertices='cross',
        size=(0.5, 0.5),
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor='white',
        opacity=None, depth=-1.0, interpolate=True)
    # set audio backend
    sound.Sound.backend = 'ptb'
    audiUR = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Laptop',    name='audiUR'
    )
    audiUR.setVolume(1.0)
    colorUR = visual.Rect(
        win=win, name='colorUR',
        width=(4, 4)[0], height=(4, 4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    audiUL = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Laptop',    name='audiUL'
    )
    audiUL.setVolume(1.0)
    colorUL = visual.Rect(
        win=win, name='colorUL',
        width=(4, 4)[0], height=(4, 4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-5.0, interpolate=True)
    audiBL = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Laptop',    name='audiBL'
    )
    audiBL.setVolume(1.0)
    colorBL = visual.Rect(
        win=win, name='colorBL',units='deg', 
        width=(4, 4)[0], height=(4, 4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-7.0, interpolate=True)
    audiBR = sound.Sound(
        'A', 
        secs=-1, 
        stereo=True, 
        hamming=True, 
        speaker='Laptop',    name='audiBR'
    )
    audiBR.setVolume(1.0)
    colorBR = visual.Rect(
        win=win, name='colorBR',units='deg', 
        width=(4, 4)[0], height=(4, 4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-9.0, interpolate=True)
    
    # --- Initialize components for Routine "cue" ---
    Cue = visual.Rect(
        win=win, name='Cue',
        width=(4,4)[0], height=(4,4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='white', fillColor=None,
        opacity=None, depth=-1.0, interpolate=True)
    targetC = visual.Rect(
        win=win, name='targetC',
        width=(4, 4)[0], height=(4, 4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetAudi = sound.Sound(
        'A', 
        secs=1.0, 
        stereo=True, 
        hamming=True, 
        speaker='Laptop',    name='targetAudi'
    )
    targetAudi.setVolume(1.0)
    
    # --- Initialize components for Routine "task" ---
    BOX = visual.ImageStim(
        win=win,
        name='BOX', 
        image='stimuli/box.png', mask=None, anchor='center',
        ori=0.0, pos=(0, 0), draggable=False, size=(6, 6),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-1.0)
    UL = visual.TextStim(win=win, name='UL',
        text='',
        font='Arial',
        units='deg', pos=[0,0], draggable=False, height=4.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    UR = visual.TextStim(win=win, name='UR',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=4.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    BL = visual.TextStim(win=win, name='BL',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=4.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    BR = visual.TextStim(win=win, name='BR',
        text='',
        font='Arial',
        pos=[0,0], draggable=False, height=4.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    vUL = visual.Rect(
        win=win, name='vUL',
        width=[4,4][0], height=[4,4][1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-6.0, interpolate=True)
    vUR = visual.Rect(
        win=win, name='vUR',
        width=(4,4)[0], height=(4,4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-7.0, interpolate=True)
    vBL = visual.Rect(
        win=win, name='vBL',
        width=(4,4)[0], height=(4,4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-8.0, interpolate=True)
    vBR = visual.Rect(
        win=win, name='vBR',
        width=(4,4)[0], height=(4,4)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor=None, fillColor='white',
        opacity=None, depth=-9.0, interpolate=True)
    key_resp_2 = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "rest" ---
    rest_text = visual.TextStim(win=win, name='rest_text',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.8, wrapWidth=26, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR', alignText='left', anchorHoriz='center',
        depth=-1.0);
    rest_key = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    if eyetracker is not None:
        eyetracker.enableEventReporting()
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "Intro" ---
    # create an object to store info about Routine Intro
    Intro = data.Routine(
        name='Intro',
        components=[text, key_resp],
    )
    Intro.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp
    key_resp.keys = []
    key_resp.rt = []
    _key_resp_allKeys = []
    # store start times for Intro
    Intro.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    Intro.tStart = globalClock.getTime(format='float')
    Intro.status = STARTED
    thisExp.addData('Intro.started', Intro.tStart)
    Intro.maxDuration = None
    # keep track of which components have finished
    IntroComponents = Intro.components
    for thisComponent in Intro.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "Intro" ---
    thisExp.currentRoutine = Intro
    Intro.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *text* updates
        
        # if text is starting this frame...
        if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            text.frameNStart = frameN  # exact frame index
            text.tStart = t  # local t and not account for scr refresh
            text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'text.started')
            # update status
            text.status = STARTED
            text.setAutoDraw(True)
        
        # if text is active this frame...
        if text.status == STARTED:
            # update params
            pass
        
        # *key_resp* updates
        waitOnFlip = False
        
        # if key_resp is starting this frame...
        if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp.frameNStart = frameN  # exact frame index
            key_resp.tStart = t  # local t and not account for scr refresh
            key_resp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp.started')
            # update status
            key_resp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp.status == STARTED and not waitOnFlip:
            theseKeys = key_resp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_allKeys.extend(theseKeys)
            if len(_key_resp_allKeys):
                key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                key_resp.rt = _key_resp_allKeys[-1].rt
                key_resp.duration = _key_resp_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=Intro,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            Intro.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if Intro.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in Intro.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "Intro" ---
    for thisComponent in Intro.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for Intro
    Intro.tStop = globalClock.getTime(format='float')
    Intro.tStopRefresh = tThisFlipGlobal
    thisExp.addData('Intro.stopped', Intro.tStop)
    # check responses
    if key_resp.keys in ['', [], None]:  # No response was made
        key_resp.keys = None
    thisExp.addData('key_resp.keys',key_resp.keys)
    if key_resp.keys != None:  # we had a response
        thisExp.addData('key_resp.rt', key_resp.rt)
        thisExp.addData('key_resp.duration', key_resp.duration)
    thisExp.nextEntry()
    # the Routine "Intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

    # ══════════════════════════════════════════════════════════════════
    #
    #
    #     P(r=1|x) = δ/2 + (1-δ)·[1 - Φ((α-x)/β)]
    #
    # ══════════════════════════════════════════════════════════════════
    # ══════════════════════════════════════════════════════════════════
    from AGRT import AGRTHandler

    OVERALL_ACC = 0.64
    LAPSE       = 0.08
    from snr_runtime import SNRStimulus

    SND_TOKEN   = 'be'
    SNR_LIM     = 18.0
    SNR_NAMES   = ['hi_snr', 'lo_snr']
    SND_LABELS  = ['[bi]', '[pi]']
    ITEM_SNR    = [0, 0, 1, 1]
    AUDIO_HI, AUDIO_LO = +6.0, -6.0
    _ARC_LIM = float(min(-_LUT_ARC[0], _LUT_ARC[-1]))

    ADAPT_FIX_ARC = 0.0
    ADAPT_FIX_SNR = 12.0

    #
    SND_FEEDBACK = True

    snd = SNRStimulus(outdir=filename + '_snr', token=SND_TOKEN)

    # ══════════════════════════════════════════════════════════════════
    #
    #
    # ══════════════════════════════════════════════════════════════════
    MASK_DUR      = 0.3
    MASK_VISUAL   = True
    MASK_AUDIO    = True
    MASK_NOISE_DB = 0.0
    MASK_TEX_N    = 32
    MASK_SIZE     = 4.0

    import snr_audio
    def _mask_ref_rms(n_seeds=16):
        _v = []
        for _s in range(n_seeds):
            _sr, _sp, _nz, _lead = snr_audio.mix_components(
                SND_TOKEN, 0.0, np.random.default_rng(_s))
            _tail = int(round(snr_audio.NOISE_TAIL_MS * _sr / 1000.0))
            _v.append(float(np.mean(_nz[_lead:len(_nz) - _tail] ** 2)))
        return _sr, float(np.sqrt(np.mean(_v)))
    MASK_SR, MASK_REF_RMS = _mask_ref_rms()
    MASK_N_SAMP = int(round(MASK_DUR * MASK_SR))
    print(f"[mask] {MASK_DUR}s visual={MASK_VISUAL} audio={MASK_AUDIO};"
          f" 0 dB SNR noise reference RMS={MASK_REF_RMS:.4f}, offset {MASK_NOISE_DB:+.1f} dB")

    def make_mask_noise(trial_idx):
        """Generate a MASK_DUR-second speech-shaped noise burst for this trial with a fresh seed, write it as a wav, and return (seed, db, rms, path, summary)."""
        _seed = snr_audio.new_seed()
        _db   = float(MASK_NOISE_DB)
        _rms  = MASK_REF_RMS * 10.0 ** (_db / 20.0)
        _y    = snr_audio.speech_shaped_noise(
            MASK_N_SAMP, np.random.default_rng(_seed)) * _rms
        _name = f"mask_{trial_idx:04d}_{_db:+.2f}dB.wav"
        _path = os.path.join(snd.outdir, _name)
        _scale = snr_audio.write_wav(_path, MASK_SR, _y)
        _summary = f"ssn|{_db:+.2f}dB|seed={_seed}|{_name}|scale={_scale:.3f}"
        return _seed, _db, _rms, _path, _summary

    # --- Initialize components for Routine "mask" ---
    MASK_VIS_STIMS = []
    for _q, _nm in enumerate(['maskUR', 'maskUL', 'maskBL', 'maskBR']):
        MASK_VIS_STIMS.append(visual.GratingStim(
            win=win, name=_nm, units='deg',
            tex=np.zeros((MASK_TEX_N, MASK_TEX_N)), mask=None,
            size=(MASK_SIZE, MASK_SIZE), sf=1.0 / MASK_SIZE, phase=0.0,
            ori=0.0, pos=(0, 0),
            color=[1, 1, 1], colorSpace='rgb', contrast=1.0, opacity=None,
            interpolate=False, depth=-1.0 - _q))
    maskUR, maskUL, maskBL, maskBR = MASK_VIS_STIMS
    maskAudi = sound.Sound(
        'A',
        secs=MASK_DUR,
        stereo=True,
        hamming=True,
        speaker='Laptop',    name='maskAudi'
    )
    maskAudi.setVolume(1.0)

    adapt_text = visual.TextStim(win=win, name='adapt_text', text='',
                                 height=0.8, color='white', pos=(0, 0), wrapWidth=26,
                                 alignText='left', anchorHoriz='center')
    fb_frame = visual.Rect(
        win=win, name='fb_frame', width=7.0, height=9.5,
        ori=0.0, pos=(0, 0), anchor='center', lineWidth=4.0,
        lineColor='white', fillColor=None, interpolate=True)

    agrt = AGRTHandler(nTrials=N_ADAPT_COL + N_ADAPT_SND, lapse=LAPSE,
                       dim1range=[-_ARC_LIM, _ARC_LIM],
                       dim2range=[-SNR_LIM, SNR_LIM],
                       dim1steps=100, dim2steps=100)
    COLOUR_ARC = [ADAPT_FIX_ARC, ADAPT_FIX_ARC]
    COLOUR_HEX = [colour_for(COLOUR_ARC[0]), colour_for(COLOUR_ARC[1])]
    AUDIO_HI, AUDIO_LO = ADAPT_FIX_SNR, ADAPT_FIX_SNR
    print(f"[plan] calibration: block 1 colour {N_ADAPT_COL} trials, block 2 sound {N_ADAPT_SND} trials, all with the full task")

    # --- Prepare to start Routine "instruction_normal" ---
    # create an object to store info about Routine instruction_normal
    instruction_normal = data.Routine(
        name='instruction_normal',
        components=[instruction_normal_text, instruction_normal_key],
    )
    instruction_normal.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for instruction_normal_key
    instruction_normal_key.keys = []
    instruction_normal_key.rt = []
    _instruction_normal_key_allKeys = []
    # store start times for instruction_normal
    instruction_normal.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    instruction_normal.tStart = globalClock.getTime(format='float')
    instruction_normal.status = STARTED
    thisExp.addData('instruction_normal.started', instruction_normal.tStart)
    instruction_normal.maxDuration = None
    # keep track of which components have finished
    instruction_normalComponents = instruction_normal.components
    for thisComponent in instruction_normal.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    instruction_key_img.setAutoDraw(True)
    # --- Run Routine "instruction_normal" ---
    thisExp.currentRoutine = instruction_normal
    instruction_normal.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *instruction_normal_text* updates
        
        # if instruction_normal_text is starting this frame...
        if instruction_normal_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instruction_normal_text.frameNStart = frameN  # exact frame index
            instruction_normal_text.tStart = t  # local t and not account for scr refresh
            instruction_normal_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instruction_normal_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instruction_normal_text.started')
            # update status
            instruction_normal_text.status = STARTED
            instruction_normal_text.setAutoDraw(True)
        
        # if instruction_normal_text is active this frame...
        if instruction_normal_text.status == STARTED:
            # update params
            pass
        
        # *instruction_normal_key* updates
        waitOnFlip = False
        
        # if instruction_normal_key is starting this frame...
        if instruction_normal_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            instruction_normal_key.frameNStart = frameN  # exact frame index
            instruction_normal_key.tStart = t  # local t and not account for scr refresh
            instruction_normal_key.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(instruction_normal_key, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'instruction_normal_key.started')
            # update status
            instruction_normal_key.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(instruction_normal_key.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(instruction_normal_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if instruction_normal_key.status == STARTED and not waitOnFlip:
            theseKeys = instruction_normal_key.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _instruction_normal_key_allKeys.extend(theseKeys)
            if len(_instruction_normal_key_allKeys):
                instruction_normal_key.keys = _instruction_normal_key_allKeys[-1].name  # just the last key pressed
                instruction_normal_key.rt = _instruction_normal_key_allKeys[-1].rt
                instruction_normal_key.duration = _instruction_normal_key_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=["escape"]):
            thisExp.status = FINISHED
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer, globalClock], 
                currentRoutine=instruction_normal,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            instruction_normal.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if instruction_normal.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in instruction_normal.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    instruction_key_img.setAutoDraw(False)
    # --- Ending Routine "instruction_normal" ---
    for thisComponent in instruction_normal.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for instruction_normal
    instruction_normal.tStop = globalClock.getTime(format='float')
    instruction_normal.tStopRefresh = tThisFlipGlobal
    thisExp.addData('instruction_normal.stopped', instruction_normal.tStop)
    thisExp.nextEntry()
    # the Routine "instruction_normal" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=N_TRIALS, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
        isTrials=False, 
    )
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    
    for thisTrial in trials:
        trials.status = STARTED
        if hasattr(thisTrial, 'status'):
            thisTrial.status = STARTED
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "study" ---
        # create an object to store info about Routine study
        study = data.Routine(
            name='study',
            components=[Fixation, audiUR, colorUR, audiUL, colorUL, audiBL, colorBL, audiBR, colorBR],
        )
        study.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from pattern
        trial_i += 1
        cue_valid, target_item, relation, target_serial = trial_plan[trial_i]
        phase = ('adapt_col' if trial_i < N_ADAPT_COL else
                 'adapt_snd' if trial_i < N_ADAPT     else
                 'practice'  if trial_i < N_PRE       else 'main')
        is_practice = (phase == 'practice')
        is_adapt    = phase.startswith('adapt')

        adapt_x = None
        if phase == 'adapt_col':
            adapt_x = float(agrt._psi1.nextIntensity)
            COLOUR_ARC = [-abs(adapt_x), abs(adapt_x)]
            COLOUR_HEX = [colour_for(COLOUR_ARC[0]), colour_for(COLOUR_ARC[1])]
            AUDIO_HI, AUDIO_LO = ADAPT_FIX_SNR, ADAPT_FIX_SNR
            _cb = 1 if adapt_x > 0 else 0
            _sb = int(rng.integers(2))
            target_item = _cb + 2 * _sb
        elif phase == 'adapt_snd':
            adapt_x = float(agrt._psi2.nextIntensity)
            AUDIO_HI, AUDIO_LO = abs(adapt_x), -abs(adapt_x)
            COLOUR_ARC = [ADAPT_FIX_ARC, ADAPT_FIX_ARC]
            COLOUR_HEX = [colour_for(COLOUR_ARC[0]), colour_for(COLOUR_ARC[1])]
            _sb = 0 if adapt_x > 0 else 1
            _cb = int(rng.integers(2))
            target_item = _cb + 2 * _sb
        
        SNR_LEVELS = [AUDIO_HI, AUDIO_LO]                  # index 0 = hi_snr([bi]), 1 = lo_snr([pi])
        itemAudi   = snd.make_many([SNR_LEVELS[ITEM_SNR[_i]] for _i in range(4)],
                                   tags=[f'item{_i}' for _i in range(4)])
        itemColhex = [COLOUR_HEX[0], COLOUR_HEX[1], COLOUR_HEX[0], COLOUR_HEX[1]]
        Fix_Dur = .3
        
        d = 10.0 / np.sqrt(2)
        POS   = [( d,  d),
                 (-d,  d),
                 (-d, -d),
                 ( d, -d)]
        NAMES = ['UR', 'UL', 'BL', 'BR']
        START = [0.3, 1.3, 2.3, 3.3]
        DUR   = 1.0
        
        posURx, posURy = POS[0]
        posULx, posULy = POS[1]
        posBLx, posBLy = POS[2]
        posBRx, posBRy = POS[3]
        
        quad_content = [int(x) for x in rng.permutation(4)]
        target_quad  = quad_content.index(target_item)
        
        time_perm = [int(x) for x in rng.permutation(4)]
        _i = time_perm.index(target_serial)
        time_perm[_i], time_perm[target_quad] = time_perm[target_quad], time_perm[_i]
        
        StudyUR, itemAudiUR = itemColhex[quad_content[0]], itemAudi[quad_content[0]]
        StudyUL, itemAudiUL = itemColhex[quad_content[1]], itemAudi[quad_content[1]]
        StudyBL, itemAudiBL = itemColhex[quad_content[2]], itemAudi[quad_content[2]]
        StudyBR, itemAudiBR = itemColhex[quad_content[3]], itemAudi[quad_content[3]]
        
        TimeStartUR = START[time_perm[0]]
        TimeStartUL = START[time_perm[1]]
        TimeStartBL = START[time_perm[2]]
        TimeStartBR = START[time_perm[3]]
        
        audiUR.setSound(itemAudiUR, secs=DUR, hamming=True)
        audiUR.setVolume(1.0, log=False)
        audiUR.seek(0)
        colorUR.setFillColor(StudyUR)
        colorUR.setPos((posURx, posURy))
        audiUL.setSound(itemAudiUL, secs=DUR, hamming=True)
        audiUL.setVolume(1.0, log=False)
        audiUL.seek(0)
        colorUL.setFillColor(StudyUL)
        colorUL.setPos((posULx, posULy))
        audiBL.setSound(itemAudiBL, secs=DUR, hamming=True)
        audiBL.setVolume(1.0, log=False)
        audiBL.seek(0)
        colorBL.setFillColor(StudyBL)
        colorBL.setPos((posBLx, posBLy))
        audiBR.setSound(itemAudiBR, secs=DUR, hamming=True)
        audiBR.setVolume(1.0, log=False)
        audiBR.seek(0)
        colorBR.setFillColor(StudyBR)
        colorBR.setPos((posBRx, posBRy))
        mask_vis_seed = mask_noise_seed = mask_noise_db = mask_noise_rms = None
        mask_noise_summary = ''
        if MASK_VISUAL:
            mask_vis_seed = snr_audio.new_seed()
            _mrng = np.random.default_rng(mask_vis_seed)
            for _q, _mk in enumerate(MASK_VIS_STIMS):
                _mk.setTex(_mrng.uniform(-1.0, 1.0, (MASK_TEX_N, MASK_TEX_N)))
                _mk.setPos(POS[_q])
        if MASK_AUDIO:
            (mask_noise_seed, mask_noise_db, mask_noise_rms,
             _mask_wav, mask_noise_summary) = make_mask_noise(trial_i)
            maskAudi.setSound(_mask_wav, secs=MASK_DUR, hamming=True)
            maskAudi.setVolume(1.0, log=False)
            maskAudi.seek(0)
        # store start times for study
        study.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study.tStart = globalClock.getTime(format='float')
        study.status = STARTED
        thisExp.addData('study.started', study.tStart)
        study.maxDuration = None
        # keep track of which components have finished
        studyComponents = study.components
        for thisComponent in study.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "study" ---
        thisExp.currentRoutine = study
        study.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fixation* updates
            
            # if Fixation is starting this frame...
            if Fixation.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fixation.frameNStart = frameN  # exact frame index
                Fixation.tStart = t  # local t and not account for scr refresh
                Fixation.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fixation, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fixation.started')
                # update status
                Fixation.status = STARTED
                Fixation.setAutoDraw(True)
            
            # if Fixation is active this frame...
            if Fixation.status == STARTED:
                # update params
                pass
            
            # if Fixation is stopping this frame...
            if Fixation.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fixation.tStartRefresh + Fix_Dur-frameTolerance:
                    # keep track of stop time/frame for later
                    Fixation.tStop = t  # not accounting for scr refresh
                    Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                    Fixation.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fixation.stopped')
                    # update status
                    Fixation.status = FINISHED
                    Fixation.setAutoDraw(False)
            
            # *audiUR* updates
            
            # if audiUR is starting this frame...
            if audiUR.status == NOT_STARTED and tThisFlip >= TimeStartUR-frameTolerance:
                # keep track of start time/frame for later
                audiUR.frameNStart = frameN  # exact frame index
                audiUR.tStart = t  # local t and not account for scr refresh
                audiUR.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audiUR.started', tThisFlipGlobal)
                # update status
                audiUR.status = STARTED
                audiUR.play(when=win)  # sync with win flip
            
            # if audiUR is stopping this frame...
            if audiUR.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audiUR.tStartRefresh + DUR-frameTolerance or audiUR.isFinished:
                    # keep track of stop time/frame for later
                    audiUR.tStop = t  # not accounting for scr refresh
                    audiUR.tStopRefresh = tThisFlipGlobal  # on global time
                    audiUR.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audiUR.stopped')
                    # update status
                    audiUR.status = FINISHED
                    audiUR.stop()
            
            # *colorUR* updates
            
            # if colorUR is starting this frame...
            if colorUR.status == NOT_STARTED and tThisFlip >= TimeStartUR-frameTolerance:
                # keep track of start time/frame for later
                colorUR.frameNStart = frameN  # exact frame index
                colorUR.tStart = t  # local t and not account for scr refresh
                colorUR.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(colorUR, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colorUR.started')
                # update status
                colorUR.status = STARTED
                colorUR.setAutoDraw(True)
            
            # if colorUR is active this frame...
            if colorUR.status == STARTED:
                # update params
                pass
            
            # if colorUR is stopping this frame...
            if colorUR.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > colorUR.tStartRefresh + DUR-frameTolerance:
                    # keep track of stop time/frame for later
                    colorUR.tStop = t  # not accounting for scr refresh
                    colorUR.tStopRefresh = tThisFlipGlobal  # on global time
                    colorUR.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colorUR.stopped')
                    # update status
                    colorUR.status = FINISHED
                    colorUR.setAutoDraw(False)
            
            # *audiUL* updates
            
            # if audiUL is starting this frame...
            if audiUL.status == NOT_STARTED and tThisFlip >= TimeStartUL-frameTolerance:
                # keep track of start time/frame for later
                audiUL.frameNStart = frameN  # exact frame index
                audiUL.tStart = t  # local t and not account for scr refresh
                audiUL.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audiUL.started', tThisFlipGlobal)
                # update status
                audiUL.status = STARTED
                audiUL.play(when=win)  # sync with win flip
            
            # if audiUL is stopping this frame...
            if audiUL.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audiUL.tStartRefresh + DUR-frameTolerance or audiUL.isFinished:
                    # keep track of stop time/frame for later
                    audiUL.tStop = t  # not accounting for scr refresh
                    audiUL.tStopRefresh = tThisFlipGlobal  # on global time
                    audiUL.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audiUL.stopped')
                    # update status
                    audiUL.status = FINISHED
                    audiUL.stop()
            
            # *colorUL* updates
            
            # if colorUL is starting this frame...
            if colorUL.status == NOT_STARTED and tThisFlip >= TimeStartUL-frameTolerance:
                # keep track of start time/frame for later
                colorUL.frameNStart = frameN  # exact frame index
                colorUL.tStart = t  # local t and not account for scr refresh
                colorUL.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(colorUL, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colorUL.started')
                # update status
                colorUL.status = STARTED
                colorUL.setAutoDraw(True)
            
            # if colorUL is active this frame...
            if colorUL.status == STARTED:
                # update params
                pass
            
            # if colorUL is stopping this frame...
            if colorUL.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > colorUL.tStartRefresh + DUR-frameTolerance:
                    # keep track of stop time/frame for later
                    colorUL.tStop = t  # not accounting for scr refresh
                    colorUL.tStopRefresh = tThisFlipGlobal  # on global time
                    colorUL.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colorUL.stopped')
                    # update status
                    colorUL.status = FINISHED
                    colorUL.setAutoDraw(False)
            
            # *audiBL* updates
            
            # if audiBL is starting this frame...
            if audiBL.status == NOT_STARTED and tThisFlip >= TimeStartBL-frameTolerance:
                # keep track of start time/frame for later
                audiBL.frameNStart = frameN  # exact frame index
                audiBL.tStart = t  # local t and not account for scr refresh
                audiBL.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audiBL.started', tThisFlipGlobal)
                # update status
                audiBL.status = STARTED
                audiBL.play(when=win)  # sync with win flip
            
            # if audiBL is stopping this frame...
            if audiBL.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audiBL.tStartRefresh + DUR-frameTolerance or audiBL.isFinished:
                    # keep track of stop time/frame for later
                    audiBL.tStop = t  # not accounting for scr refresh
                    audiBL.tStopRefresh = tThisFlipGlobal  # on global time
                    audiBL.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audiBL.stopped')
                    # update status
                    audiBL.status = FINISHED
                    audiBL.stop()
            
            # *colorBL* updates
            
            # if colorBL is starting this frame...
            if colorBL.status == NOT_STARTED and tThisFlip >= TimeStartBL-frameTolerance:
                # keep track of start time/frame for later
                colorBL.frameNStart = frameN  # exact frame index
                colorBL.tStart = t  # local t and not account for scr refresh
                colorBL.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(colorBL, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colorBL.started')
                # update status
                colorBL.status = STARTED
                colorBL.setAutoDraw(True)
            
            # if colorBL is active this frame...
            if colorBL.status == STARTED:
                # update params
                pass
            
            # if colorBL is stopping this frame...
            if colorBL.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > colorBL.tStartRefresh + DUR-frameTolerance:
                    # keep track of stop time/frame for later
                    colorBL.tStop = t  # not accounting for scr refresh
                    colorBL.tStopRefresh = tThisFlipGlobal  # on global time
                    colorBL.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colorBL.stopped')
                    # update status
                    colorBL.status = FINISHED
                    colorBL.setAutoDraw(False)
            
            # *audiBR* updates
            
            # if audiBR is starting this frame...
            if audiBR.status == NOT_STARTED and tThisFlip >= TimeStartBR-frameTolerance:
                # keep track of start time/frame for later
                audiBR.frameNStart = frameN  # exact frame index
                audiBR.tStart = t  # local t and not account for scr refresh
                audiBR.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audiBR.started', tThisFlipGlobal)
                # update status
                audiBR.status = STARTED
                audiBR.play(when=win)  # sync with win flip
            
            # if audiBR is stopping this frame...
            if audiBR.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audiBR.tStartRefresh + DUR-frameTolerance or audiBR.isFinished:
                    # keep track of stop time/frame for later
                    audiBR.tStop = t  # not accounting for scr refresh
                    audiBR.tStopRefresh = tThisFlipGlobal  # on global time
                    audiBR.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audiBR.stopped')
                    # update status
                    audiBR.status = FINISHED
                    audiBR.stop()
            
            # *colorBR* updates
            
            # if colorBR is starting this frame...
            if colorBR.status == NOT_STARTED and tThisFlip >= TimeStartBR-frameTolerance:
                # keep track of start time/frame for later
                colorBR.frameNStart = frameN  # exact frame index
                colorBR.tStart = t  # local t and not account for scr refresh
                colorBR.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(colorBR, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'colorBR.started')
                # update status
                colorBR.status = STARTED
                colorBR.setAutoDraw(True)
            
            # if colorBR is active this frame...
            if colorBR.status == STARTED:
                # update params
                pass
            
            # if colorBR is stopping this frame...
            if colorBR.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > colorBR.tStartRefresh + DUR-frameTolerance:
                    # keep track of stop time/frame for later
                    colorBR.tStop = t  # not accounting for scr refresh
                    colorBR.tStopRefresh = tThisFlipGlobal  # on global time
                    colorBR.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'colorBR.stopped')
                    # update status
                    colorBR.status = FINISHED
                    colorBR.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=study,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study" ---
        for thisComponent in study.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study
        study.tStop = globalClock.getTime(format='float')
        study.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study.stopped', study.tStop)
        # Run 'End Routine' code from pattern
        thisExp.addData('phase',         phase)
        thisExp.addData('is_practice',   bool(is_practice))
        thisExp.addData('trial_i',       trial_i)
        thisExp.addData('colour_arc_lo', COLOUR_ARC[0])
        thisExp.addData('colour_arc_hi', COLOUR_ARC[1])
        thisExp.addData('snr_hi',        AUDIO_HI)
        thisExp.addData('snr_lo',        AUDIO_LO)
        thisExp.addData('quad_content',  str(quad_content))
        thisExp.addData('time_perm',     str(time_perm))
        thisExp.addData('target_serial', int(target_serial))
        thisExp.addData('studyUR', f'{StudyUR}|{itemAudiUR}|t={TimeStartUR}')
        thisExp.addData('studyUL', f'{StudyUL}|{itemAudiUL}|t={TimeStartUL}')
        thisExp.addData('studyBL', f'{StudyBL}|{itemAudiBL}|t={TimeStartBL}')
        thisExp.addData('studyBR', f'{StudyBR}|{itemAudiBR}|t={TimeStartBR}')
        
        audiUR.pause()  # ensure sound has stopped at end of Routine
        audiUL.pause()  # ensure sound has stopped at end of Routine
        audiBL.pause()  # ensure sound has stopped at end of Routine
        audiBR.pause()  # ensure sound has stopped at end of Routine
        # the Routine "study" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "mask" ---
        mask = data.Routine(
            name='mask',
            components=((list(MASK_VIS_STIMS) if MASK_VISUAL else []) +
                        ([maskAudi] if MASK_AUDIO else [])),
        )
        mask.status = NOT_STARTED
        continueRoutine = bool(mask.components)
        # store start times for mask
        mask.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        mask.tStart = globalClock.getTime(format='float')
        mask.status = STARTED
        thisExp.addData('mask.started', mask.tStart)
        mask.maxDuration = None
        # keep track of which components have finished
        maskComponents = mask.components
        for thisComponent in mask.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1

        # --- Run Routine "mask" ---
        thisExp.currentRoutine = mask
        mask.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *maskUR / maskUL / maskBL / maskBR* updates
            for _mk in (MASK_VIS_STIMS if MASK_VISUAL else []):
                # if _mk is starting this frame...
                if _mk.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    _mk.frameNStart = frameN  # exact frame index
                    _mk.tStart = t  # local t and not account for scr refresh
                    _mk.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(_mk, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, _mk.name + '.started')
                    # update status
                    _mk.status = STARTED
                    _mk.setAutoDraw(True)

                # if _mk is stopping this frame...
                if _mk.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > _mk.tStartRefresh + MASK_DUR-frameTolerance:
                        # keep track of stop time/frame for later
                        _mk.tStop = t  # not accounting for scr refresh
                        _mk.tStopRefresh = tThisFlipGlobal  # on global time
                        _mk.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, _mk.name + '.stopped')
                        # update status
                        _mk.status = FINISHED
                        _mk.setAutoDraw(False)

            # *maskAudi* updates
            if MASK_AUDIO:
                # if maskAudi is starting this frame...
                if maskAudi.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    maskAudi.frameNStart = frameN  # exact frame index
                    maskAudi.tStart = t  # local t and not account for scr refresh
                    maskAudi.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('maskAudi.started', tThisFlipGlobal)
                    # update status
                    maskAudi.status = STARTED
                    maskAudi.play(when=win)  # sync with win flip

                # if maskAudi is stopping this frame...
                if maskAudi.status == STARTED:
                    if tThisFlipGlobal > maskAudi.tStartRefresh + MASK_DUR + frameDur-frameTolerance or maskAudi.isFinished:
                        # keep track of stop time/frame for later
                        maskAudi.tStop = t  # not accounting for scr refresh
                        maskAudi.tStopRefresh = tThisFlipGlobal  # on global time
                        maskAudi.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'maskAudi.stopped')
                        # update status
                        maskAudi.status = FINISHED
                        maskAudi.stop()

            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp,
                    win=win,
                    timers=[routineTimer, globalClock],
                    currentRoutine=mask,
                )
                # skip the frame we paused on
                continue

            # has a Component requested the Routine to end?
            if not continueRoutine:
                mask.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if mask.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in mask.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # --- Ending Routine "mask" ---
        for thisComponent in mask.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for mask
        mask.tStop = globalClock.getTime(format='float')
        mask.tStopRefresh = tThisFlipGlobal
        thisExp.addData('mask.stopped', mask.tStop)
        _on  = [c.tStartRefresh for c in mask.components if c.tStartRefresh is not None]
        _off = [c.tStopRefresh  for c in mask.components if c.tStopRefresh  is not None]
        thisExp.addData('mask_onset',      min(_on)  if _on  else '')
        thisExp.addData('mask_offset',     max(_off) if _off else '')
        thisExp.addData('mask_dur',        MASK_DUR if mask.components else 0.0)
        thisExp.addData('mask_visual',     bool(MASK_VISUAL))
        thisExp.addData('mask_audio',      bool(MASK_AUDIO))
        thisExp.addData('mask_vis_seed',   mask_vis_seed   if MASK_VISUAL else '')
        thisExp.addData('mask_noise_seed', mask_noise_seed if MASK_AUDIO else '')
        thisExp.addData('mask_noise_db',   mask_noise_db   if MASK_AUDIO else '')
        thisExp.addData('mask_noise_rms',  mask_noise_rms  if MASK_AUDIO else '')
        thisExp.addData('mask_ref_rms',    MASK_REF_RMS)
        if MASK_AUDIO:
            thisExp.addData('snd_mask', mask_noise_summary)

        if MASK_AUDIO:
            maskAudi.pause()  # ensure sound has stopped at end of Routine
        # the Routine "mask" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        # --- Prepare to start Routine "cue" ---
        # create an object to store info about Routine cue
        cue = data.Routine(
            name='cue',
            components=[Cue, targetC, targetAudi],
        )
        cue.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from code
        cued_item = target_item ^ relation      # relation = 0 -> cued == target (valid)
        cue_idx   = quad_content.index(cued_item)
        
        cue_posx, cue_posy       = POS[cue_idx]
        target_posx, target_posy = POS[target_quad]
        POS_cue = POS[cue_idx]
        
        cue_color = itemColhex[target_item]
        cue_audi  = snd.make(SNR_LEVELS[ITEM_SNR[target_item]], tag='probe')
        
        Cue.setPos(POS_cue)
        targetC.setFillColor(cue_color)
        targetC.setPos((cue_posx,cue_posy))
        targetAudi.setSound(cue_audi, secs=1.0, hamming=True)
        targetAudi.setVolume(1.0, log=False)
        targetAudi.seek(0)
        # store start times for cue
        cue.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        cue.tStart = globalClock.getTime(format='float')
        cue.status = STARTED
        thisExp.addData('cue.started', cue.tStart)
        cue.maxDuration = None
        # keep track of which components have finished
        cueComponents = cue.components
        for thisComponent in cue.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "cue" ---
        thisExp.currentRoutine = cue
        cue.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 2.0:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Cue* updates
            
            # if Cue is starting this frame...
            if Cue.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Cue.frameNStart = frameN  # exact frame index
                Cue.tStart = t  # local t and not account for scr refresh
                Cue.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Cue, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Cue.started')
                # update status
                Cue.status = STARTED
                Cue.setAutoDraw(True)
            
            # if Cue is active this frame...
            if Cue.status == STARTED:
                # update params
                pass
            
            # if Cue is stopping this frame...
            if Cue.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Cue.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    Cue.tStop = t  # not accounting for scr refresh
                    Cue.tStopRefresh = tThisFlipGlobal  # on global time
                    Cue.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Cue.stopped')
                    # update status
                    Cue.status = FINISHED
                    Cue.setAutoDraw(False)
            
            # *targetC* updates
            
            # if targetC is starting this frame...
            if targetC.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                targetC.frameNStart = frameN  # exact frame index
                targetC.tStart = t  # local t and not account for scr refresh
                targetC.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(targetC, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'targetC.started')
                # update status
                targetC.status = STARTED
                targetC.setAutoDraw(True)
            
            # if targetC is active this frame...
            if targetC.status == STARTED:
                # update params
                pass
            
            # if targetC is stopping this frame...
            if targetC.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > targetC.tStartRefresh + 1.0-frameTolerance:
                    # keep track of stop time/frame for later
                    targetC.tStop = t  # not accounting for scr refresh
                    targetC.tStopRefresh = tThisFlipGlobal  # on global time
                    targetC.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetC.stopped')
                    # update status
                    targetC.status = FINISHED
                    targetC.setAutoDraw(False)
            
            # *targetAudi* updates
            
            # if targetAudi is starting this frame...
            if targetAudi.status == NOT_STARTED and tThisFlip >= 1-frameTolerance:
                # keep track of start time/frame for later
                targetAudi.frameNStart = frameN  # exact frame index
                targetAudi.tStart = t  # local t and not account for scr refresh
                targetAudi.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('targetAudi.started', tThisFlipGlobal)
                # update status
                targetAudi.status = STARTED
                targetAudi.play(when=win)  # sync with win flip
            
            # if targetAudi is stopping this frame...
            if targetAudi.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > targetAudi.tStartRefresh + 1.0-frameTolerance or targetAudi.isFinished:
                    # keep track of stop time/frame for later
                    targetAudi.tStop = t  # not accounting for scr refresh
                    targetAudi.tStopRefresh = tThisFlipGlobal  # on global time
                    targetAudi.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetAudi.stopped')
                    # update status
                    targetAudi.status = FINISHED
                    targetAudi.stop()
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=cue,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                cue.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if cue.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in cue.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "cue" ---
        for thisComponent in cue.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for cue
        cue.tStop = globalClock.getTime(format='float')
        cue.tStopRefresh = tThisFlipGlobal
        thisExp.addData('cue.stopped', cue.tStop)
        # Run 'End Routine' code from code
        thisExp.addData('cue_valid',     int(cue_valid))
        thisExp.addData('relation',      int(relation))
        thisExp.addData('relation_name', REL_NAME[relation])
        thisExp.addData('target_item',   int(target_item))
        thisExp.addData('cued_item',     int(cued_item))
        thisExp.addData('target_quad',   int(target_quad))
        thisExp.addData('cue_idx',       int(cue_idx))
        thisExp.addData('cue_color',     cue_color)
        thisExp.addData('cue_audi',      cue_audi)
        thisExp.addData('target_snr',    SNR_NAMES[ITEM_SNR[target_item]])
        thisExp.addData('cued_snr',      SNR_NAMES[ITEM_SNR[cued_item]])
        thisExp.addData('POS_cue',       str(POS_cue))
        thisExp.addData('target_pos',    str((target_posx, target_posy)))
        
        targetAudi.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if cue.maxDurationReached:
            routineTimer.addTime(-cue.maxDuration)
        elif cue.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-2.000000)
        
        # --- Prepare to start Routine "task" ---
        # create an object to store info about Routine task
        task = data.Routine(
            name='task',
            components=[BOX, UL, UR, BL, BR, vUL, vUR, vBL, vBR, key_resp_2],
        )
        task.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from recog
        d = 10.0 / np.sqrt(2)
        POS = [( d,  d), (-d,  d), (-d, -d), ( d, -d)]      # 0=UR 1=UL 2=BL 3=BR
        GAP = 4.2
        POS_TXT = [(x, y + GAP/2) for x, y in POS]
        POS_COL = [(x, y - GAP/2) for x, y in POS]
        
        final_value = [COLOUR_HEX[0], COLOUR_HEX[1], COLOUR_HEX[0], COLOUR_HEX[1]]
        TXT         = [SND_LABELS[0] if SNR_LEVELS[ITEM_SNR[i]] > 0 else SND_LABELS[1]
                       for i in range(4)]
        
        txtUR_pos, colUR_pos = POS_TXT[0], POS_COL[0]
        txtUL_pos, colUL_pos = POS_TXT[1], POS_COL[1]
        txtBL_pos, colBL_pos = POS_TXT[2], POS_COL[2]
        txtBR_pos, colBR_pos = POS_TXT[3], POS_COL[3]
        
        opt_perm = [int(x) for x in rng.permutation(4)]
        UR_item, UL_item, BL_item, BR_item = opt_perm
        
        UR_col, UR_TXT = final_value[UR_item], TXT[UR_item]
        UL_col, UL_TXT = final_value[UL_item], TXT[UL_item]
        BL_col, BL_TXT = final_value[BL_item], TXT[BL_item]
        BR_col, BR_TXT = final_value[BR_item], TXT[BR_item]
        
        UL.setPos(txtUL_pos)
        UL.setText(UL_TXT)
        UR.setPos(txtUR_pos)
        UR.setText(UR_TXT)
        BL.setColor('white', colorSpace='rgb')
        BL.setPos(txtBL_pos)
        BL.setText(BL_TXT)
        BR.setPos(txtBR_pos)
        BR.setText(BR_TXT)
        vUL.setFillColor(UL_col)
        vUL.setPos(colUL_pos)
        vUR.setFillColor(UR_col)
        vUR.setPos(colUR_pos)
        vBL.setFillColor(BL_col)
        vBL.setPos(colBL_pos)
        vBR.setFillColor(BR_col)
        vBR.setPos(colBR_pos)
        # create starting attributes for key_resp_2
        key_resp_2.keys = []
        key_resp_2.rt = []
        _key_resp_2_allKeys = []
        # store start times for task
        task.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        task.tStart = globalClock.getTime(format='float')
        task.status = STARTED
        thisExp.addData('task.started', task.tStart)
        task.maxDuration = None
        # keep track of which components have finished
        taskComponents = task.components
        for thisComponent in task.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "task" ---
        thisExp.currentRoutine = task
        task.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *BOX* updates
            
            # if BOX is starting this frame...
            if BOX.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                BOX.frameNStart = frameN  # exact frame index
                BOX.tStart = t  # local t and not account for scr refresh
                BOX.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(BOX, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'BOX.started')
                # update status
                BOX.status = STARTED
                BOX.setAutoDraw(True)
            
            # if BOX is active this frame...
            if BOX.status == STARTED:
                # update params
                pass
            
            # *UL* updates
            
            # if UL is starting this frame...
            if UL.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                UL.frameNStart = frameN  # exact frame index
                UL.tStart = t  # local t and not account for scr refresh
                UL.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(UL, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'UL.started')
                # update status
                UL.status = STARTED
                UL.setAutoDraw(True)
            
            # if UL is active this frame...
            if UL.status == STARTED:
                # update params
                pass
            
            # *UR* updates
            
            # if UR is starting this frame...
            if UR.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                UR.frameNStart = frameN  # exact frame index
                UR.tStart = t  # local t and not account for scr refresh
                UR.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(UR, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'UR.started')
                # update status
                UR.status = STARTED
                UR.setAutoDraw(True)
            
            # if UR is active this frame...
            if UR.status == STARTED:
                # update params
                pass
            
            # *BL* updates
            
            # if BL is starting this frame...
            if BL.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                BL.frameNStart = frameN  # exact frame index
                BL.tStart = t  # local t and not account for scr refresh
                BL.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(BL, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'BL.started')
                # update status
                BL.status = STARTED
                BL.setAutoDraw(True)
            
            # if BL is active this frame...
            if BL.status == STARTED:
                # update params
                pass
            
            # *BR* updates
            
            # if BR is starting this frame...
            if BR.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                BR.frameNStart = frameN  # exact frame index
                BR.tStart = t  # local t and not account for scr refresh
                BR.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(BR, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'BR.started')
                # update status
                BR.status = STARTED
                BR.setAutoDraw(True)
            
            # if BR is active this frame...
            if BR.status == STARTED:
                # update params
                pass
            
            # *vUL* updates
            
            # if vUL is starting this frame...
            if vUL.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                vUL.frameNStart = frameN  # exact frame index
                vUL.tStart = t  # local t and not account for scr refresh
                vUL.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(vUL, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'vUL.started')
                # update status
                vUL.status = STARTED
                vUL.setAutoDraw(True)
            
            # if vUL is active this frame...
            if vUL.status == STARTED:
                # update params
                pass
            
            # *vUR* updates
            
            # if vUR is starting this frame...
            if vUR.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                vUR.frameNStart = frameN  # exact frame index
                vUR.tStart = t  # local t and not account for scr refresh
                vUR.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(vUR, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'vUR.started')
                # update status
                vUR.status = STARTED
                vUR.setAutoDraw(True)
            
            # if vUR is active this frame...
            if vUR.status == STARTED:
                # update params
                pass
            
            # *vBL* updates
            
            # if vBL is starting this frame...
            if vBL.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                vBL.frameNStart = frameN  # exact frame index
                vBL.tStart = t  # local t and not account for scr refresh
                vBL.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(vBL, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'vBL.started')
                # update status
                vBL.status = STARTED
                vBL.setAutoDraw(True)
            
            # if vBL is active this frame...
            if vBL.status == STARTED:
                # update params
                pass
            
            # *vBR* updates
            
            # if vBR is starting this frame...
            if vBR.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                vBR.frameNStart = frameN  # exact frame index
                vBR.tStart = t  # local t and not account for scr refresh
                vBR.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(vBR, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'vBR.started')
                # update status
                vBR.status = STARTED
                vBR.setAutoDraw(True)
            
            # if vBR is active this frame...
            if vBR.status == STARTED:
                # update params
                pass
            
            # *key_resp_2* updates
            waitOnFlip = False
            
            # if key_resp_2 is starting this frame...
            if key_resp_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.tStart = t  # local t and not account for scr refresh
                key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_2.started')
                # update status
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_2.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_2.getKeys(keyList=['i','o','k','l'], ignoreKeys=["escape"], waitRelease=False)
                _key_resp_2_allKeys.extend(theseKeys)
                if len(_key_resp_2_allKeys):
                    key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                    key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                    key_resp_2.duration = _key_resp_2_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=task,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                task.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if task.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in task.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "task" ---
        for thisComponent in task.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for task
        task.tStop = globalClock.getTime(format='float')
        task.tStopRefresh = tThisFlipGlobal
        thisExp.addData('task.stopped', task.tStop)
        # Run 'End Routine' code from recog
        KEY_TO_SLOT = {'i': 'UL', 'o': 'UR', 'k': 'BL', 'l': 'BR'}
        SLOT_ITEM   = {'UR': UR_item, 'UL': UL_item, 'BL': BL_item, 'BR': BR_item}
        
        pressed_key = key_resp_2.keys
        if isinstance(pressed_key, list):
            pressed_key = pressed_key[-1] if len(pressed_key) > 0 else None
        
        if pressed_key in KEY_TO_SLOT:
            chosen_slot = KEY_TO_SLOT[pressed_key]
            chosen_item = SLOT_ITEM[chosen_slot]
        else:
            chosen_slot = None
            chosen_item = None
        
        if chosen_item is None:
            outcome = 'noresp'
        elif chosen_item == target_item:
            outcome = 'correct'
        elif chosen_item == cued_item:
            outcome = 'intrusion'
        else:
            outcome = 'other'
        
        is_correct = (outcome == 'correct')
        
        err_rel = None if (chosen_item is None or outcome == 'correct') else (chosen_item ^ target_item)
        
        thisExp.addData('opt_perm',     str(opt_perm))
        thisExp.addData('pressed_key',  pressed_key)
        thisExp.addData('chosen_slot',  chosen_slot)
        thisExp.addData('chosen_item',  chosen_item)
        thisExp.addData('outcome',      outcome)
        thisExp.addData('err_rel',      err_rel)
        thisExp.addData('err_rel_name', REL_NAME[err_rel] if err_rel else '')
        thisExp.addData('is_correct',   is_correct)
        thisExp.addData('rt',           key_resp_2.rt)

        for _row in snd.drain_log():
            thisExp.addData('snd_' + _row['tag'], _row['summary'])
        
        if is_practice and outcome == 'correct':
            practice_correct += 1

        if is_adapt and chosen_item is not None:
            if phase == 'adapt_col':
                adapt_resp = chosen_item & 1                      # 1 = pink
                agrt._psi1.update(adapt_resp)
            else:
                adapt_resp = 1 if (chosen_item >> 1) == 0 else 0  # 1 = [bi]
                agrt._psi2.update(adapt_resp)
            adapt_corr = int(adapt_resp == int(adapt_x > 0))
            outcome    = 'correct' if adapt_corr else 'other'
            is_correct = bool(adapt_corr)
            thisExp.addData('outcome',    outcome)
            thisExp.addData('is_correct', is_correct)
        else:
            adapt_resp = adapt_corr = None
        if is_adapt:
            thisExp.addData('adapt_x',    adapt_x)
            thisExp.addData('adapt_resp', adapt_resp)
            thisExp.addData('adapt_corr', adapt_corr)

        if trial_i == N_ADAPT - 1:
            _lams = agrt.estimateLambda()
            (_c_lo, _c_hi), (_s_lo, _s_hi) = agrt.estimateGRTintensities(OVERALL_ACC, _lams)
            _c_lo = float(np.clip(_c_lo, _LUT_ARC[0], _LUT_ARC[-1]))
            _c_hi = float(np.clip(_c_hi, _LUT_ARC[0], _LUT_ARC[-1]))
            _s_lo = float(np.clip(_s_lo, -SNR_LIM, SNR_LIM))
            _s_hi = float(np.clip(_s_hi, -SNR_LIM, SNR_LIM))
            COLOUR_ARC = [_c_lo, _c_hi]
            COLOUR_HEX = [colour_for(_c_lo), colour_for(_c_hi)]
            AUDIO_HI, AUDIO_LO = _s_hi, _s_lo    # HI = hi_snr([bi]), LO = lo_snr([pi])
            agrt.savePosterior(filename + '_posterior')
            thisExp.addData('psi_col_alpha', float(_lams[0][0]))
            thisExp.addData('psi_col_beta',  float(_lams[0][1]))
            thisExp.addData('psi_snd_alpha', float(_lams[1][0]))
            thisExp.addData('psi_snd_beta',  float(_lams[1][1]))
            thisExp.addData('final_colour_arc_lo', _c_lo)
            thisExp.addData('final_colour_arc_hi', _c_hi)
            thisExp.addData('final_snr_hi', AUDIO_HI)
            thisExp.addData('final_snr_lo', AUDIO_LO)
            thisExp.addData('snr_token', SND_TOKEN)
            thisExp.addData('snr_lim', SNR_LIM)
            print(f"[AGRT] colour lambda={_lams[0]}  sound lambda={_lams[1]}")
            print(f"[AGRT] COLOUR_ARC={COLOUR_ARC} -> {COLOUR_HEX}; "
                  f"SNR hi([bi])={AUDIO_HI:+.2f} lo([pi])={AUDIO_LO:+.2f} dB")

        if phase != 'main' and FEEDBACK_PRE_MAIN:
            if phase == 'adapt_col':
                _fb_ok = lambda _i: (_i & 1) == (target_item & 1)
            elif phase == 'adapt_snd':
                _fb_ok = lambda _i: (_i >> 1) == (target_item >> 1)
            else:
                _fb_ok = lambda _i: _i == target_item
            _slot_pos = {'UR': POS[0], 'UL': POS[1], 'BL': POS[2], 'BR': POS[3]}
            for _st in (vUL, vUR, vBL, vBR, UL, UR, BL, BR):
                _st.draw()
            for _s, _i in SLOT_ITEM.items():
                if _fb_ok(_i):
                    fb_frame.setPos(_slot_pos[_s])
                    fb_frame.draw()
            adapt_text.text = ('Correct' if is_correct else
                               'No response' if chosen_item is None else 'Wrong')
            adapt_text.text += '\nThe correct option is framed.'
            adapt_text.draw()
            win.flip()
            core.wait(FEEDBACK_SEC)
            win.flip()
            core.wait(0.3)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys = None
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt)
            trials.addData('key_resp_2.duration', key_resp_2.duration)
        # the Routine "task" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "rest" ---
        # create an object to store info about Routine rest
        rest = data.Routine(
            name='rest',
            components=[rest_text, rest_key],
        )
        rest.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from rest_code
        n_done = trial_i + 1
        
        if n_done == N_ADAPT_COL:
            rest_msg = (
                "Part 1 (colour calibration) finished.\n\n"
                "Part 2 is the same task; this time the sounds are adjusted "
                "and all the squares have the same colour.\n\n"
                "Take a short rest.\n\n"
                "Press the space bar when you are ready to continue.")
        elif n_done == N_ADAPT:
            rest_msg = (
                "Part 2 (sound calibration) finished.\n\n"
                f"Next is a short practice of {N_PRACTICE} trials with the "
                "colours and sounds set for you. The correct option is still "
                "framed after each answer.\n\n"
                "Press the space bar when you are ready to continue.")
        elif n_done == N_PRE:
            pct = 100.0 * practice_correct / max(N_PRACTICE, 1)
            rest_msg = (
                "Practice finished.\n\n"
                f"You got {practice_correct} of {N_PRACTICE} correct ({pct:.0f}%).\n\n"
                "If that felt like guessing, tell the experimenter now.\n\n"
                "The main experiment starts next. There is no more feedback. "
                f"It is divided into {n_blocks} blocks with a rest after each one.\n\n"
                "        i = upper left            o = upper right\n"
                "        k = lower left            l = lower right\n\n"
                "Press the space bar to begin.")
        elif n_done > N_PRE and (n_done - N_PRE) % BLOCK_SIZE == 0 and n_done < N_TRIALS:
            done_blocks = (n_done - N_PRE) // BLOCK_SIZE
            rest_msg = (
                f"Block {done_blocks} of {n_blocks} finished.\n\n"
                "Take a rest. Look away from the screen for a moment.\n\n"
                "        i = upper left            o = upper right\n"
                "        k = lower left            l = lower right\n\n"
                "Press the space bar when you are ready to continue.")
        else:
            continueRoutine = False
            rest_msg = ""

        rest_text.setText(rest_msg)
        # create starting attributes for rest_key
        rest_key.keys = []
        rest_key.rt = []
        _rest_key_allKeys = []
        # store start times for rest
        rest.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        rest.tStart = globalClock.getTime(format='float')
        rest.status = STARTED
        thisExp.addData('rest.started', rest.tStart)
        rest.maxDuration = None
        # keep track of which components have finished
        restComponents = rest.components
        for thisComponent in rest.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "rest" ---
        thisExp.currentRoutine = rest
        rest.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # if trial has changed, end Routine now
            if hasattr(thisTrial, 'status') and thisTrial.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *rest_text* updates
            
            # if rest_text is starting this frame...
            if rest_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rest_text.frameNStart = frameN  # exact frame index
                rest_text.tStart = t  # local t and not account for scr refresh
                rest_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rest_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rest_text.started')
                # update status
                rest_text.status = STARTED
                rest_text.setAutoDraw(True)
            
            # if rest_text is active this frame...
            if rest_text.status == STARTED:
                # update params
                pass
            
            # *rest_key* updates
            waitOnFlip = False
            
            # if rest_key is starting this frame...
            if rest_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                rest_key.frameNStart = frameN  # exact frame index
                rest_key.tStart = t  # local t and not account for scr refresh
                rest_key.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(rest_key, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'rest_key.started')
                # update status
                rest_key.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(rest_key.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(rest_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if rest_key.status == STARTED and not waitOnFlip:
                theseKeys = rest_key.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
                _rest_key_allKeys.extend(theseKeys)
                if len(_rest_key_allKeys):
                    rest_key.keys = _rest_key_allKeys[-1].name  # just the last key pressed
                    rest_key.rt = _rest_key_allKeys[-1].rt
                    rest_key.duration = _rest_key_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer, globalClock], 
                    currentRoutine=rest,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                rest.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if rest.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in rest.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "rest" ---
        for thisComponent in rest.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for rest
        rest.tStop = globalClock.getTime(format='float')
        rest.tStopRefresh = tThisFlipGlobal
        thisExp.addData('rest.stopped', rest.tStop)
        # the Routine "rest" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        # mark thisTrial as finished
        if hasattr(thisTrial, 'status'):
            thisTrial.status = FINISHED
        # if awaiting a pause, pause now
        if trials.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            trials.status = STARTED
        thisExp.nextEntry()
    # completed N_TRIALS repeats of 'trials'
    trials.status = FINISHED
    
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    # stop any playback components
    if thisExp.currentRoutine is not None:
        for comp in thisExp.currentRoutine.getPlaybackComponents():
            comp.stop()
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    # run any 'at exit' functions
    for fcn in runAtExit:
        fcn()
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
