#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2026.1.3),
    on April 28, 2026, at 13:07
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
prefs.hardware['audioDevice'] =['Speakers (Realtek(R) Audio)']
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

# 音訊輸出裝置：交給 audio_pick.py（列出裝置、實際試開、優先耳機）。
# 換到新電腦先跑 `python audio_pick.py` 看有哪些裝置；指定裝置三選一：
#   --audio-device "名稱"、環境變數 VAWM_AUDIO_DEVICE、或 `python audio_pick.py --set "名稱"`。
# --require-headphones = 自動挑時找不到耳機就停下，不退回喇叭；--list-audio = 只列裝置就結束。
from audio_pick import setup_from_argv
AUDIO = setup_from_argv(sys.argv)



from psychtoolbox import audio
from soundfile import SoundFile
import csv

# --- Load rule.csv for feedback logic ---
def load_rules(rule_path):
    """Load rule.csv and return a lookup dictionary"""
    rules = {}
    with open(rule_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            col_type = row['targetCol'].strip()
            aud_type = row['targetAud'].strip()
            response = row['ResponseBox'].strip()
            acc = int(row['Acc'].strip())
            resp_text = row['resp'].strip().strip('"')
            key = (col_type, aud_type, response)
            rules[key] = {'Acc': acc, 'resp': resp_text}
    return rules

def get_probe_types(targetCol, targetAud, trial_data):
    """Determine the type of color and audio shown in probe"""
    # Determine color type
    if targetCol == trial_data.get('color1_target'):
        col_type = 'color1_target'
    elif targetCol == trial_data.get('color2_target'):
        col_type = 'color2_target'
    elif targetCol == trial_data.get('color1_H'):
        col_type = 'color1_H'
    elif targetCol == trial_data.get('color1_L'):
        col_type = 'color1_L'
    elif targetCol == trial_data.get('color2_H'):
        col_type = 'color2_H'
    elif targetCol == trial_data.get('color2_L'):
        col_type = 'color2_L'
    else:
        col_type = 'unknown'

    # Determine audio type
    if targetAud == trial_data.get('audio1_target_file'):
        aud_type = 'audio1_target_file'
    elif targetAud == trial_data.get('audio2_target_file'):
        aud_type = 'audio2_target_file'
    elif targetAud == trial_data.get('audio1_H_file'):
        aud_type = 'audio1_H_file'
    elif targetAud == trial_data.get('audio1_L_file'):
        aud_type = 'audio1_L_file'
    elif targetAud == trial_data.get('audio2_H_file'):
        aud_type = 'audio2_H_file'
    elif targetAud == trial_data.get('audio2_L_file'):
        aud_type = 'audio2_L_file'
    else:
        aud_type = 'unknown'

    return col_type, aud_type

def generate_stratified_conditions():
    """Generate 9 stratified probe conditions with guaranteed proportions.

    Distribution:
    - AA (conditions 0,1): 2 trials (22%)
    - HA (conditions 2,3): 1 trial (11%)
    - LA (conditions 4,5): 1 trial (11%)
    - AH (conditions 6,7): 1 trial (11%)
    - AL (conditions 12,13): 1 trial (11%)
    - HH/LH/HL/LL (conditions 8-11, 14-17): 3 trials (33%)
    """
    conditions = []
    # AA: 2 trials (25% target)
    conditions.extend([np.random.choice([0, 1]) for _ in range(2)])
    # HA: 1 trial
    conditions.append(np.random.choice([2, 3]))
    # LA: 1 trial
    conditions.append(np.random.choice([4, 5]))
    # AH: 1 trial
    conditions.append(np.random.choice([6, 7]))
    # AL: 1 trial
    conditions.append(np.random.choice([12, 13]))
    # HH/LH/HL/LL: 3 trials (split among 8 conditions)
    conditions.extend([np.random.choice([8, 9, 10, 11, 14, 15, 16, 17]) for _ in range(3)])
    # Shuffle to randomize order
    np.random.shuffle(conditions)
    return conditions

# Load rules at startup
_rule_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rule.csv')
FEEDBACK_RULES = load_rules(_rule_path)

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2026.1.3'
expName = 'VAWM'  # from the Builder filename that created this script
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
        originPath='C:\\Users\\spt904\\OneDrive - University of Texas at San Antonio\\Desktop\\VAWM\\VAWM.py',
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
            monitor='testMonitor', color='#808080', colorSpace='hex',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = '#808080'
        win.colorSpace = 'hex'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
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
    deviceManager.addDevice(
            deviceClass='psychopy.hardware.speaker.SpeakerDevice', deviceName='Speakers (Realtek(R) Audio)', index=6
        )
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
    
    # --- Initialize components for Routine "studyintro" ---
    # Run 'Begin Experiment' code from code_2
    from psychtoolbox import audio
    from soundfile import SoundFile
    

    intro = visual.TextStim(win=win, name='intro',
        text='Thank you for participating in this experiment.\nIn this task, you will see colored patches on the screen and hear two sounds through the headphones. Please remember both what you see and what you hear.\nAfterward, you will be shown one colored patch and hear one sound. If they match what you remembered, press the [Yes] key. Otherwise, press the [No] key.\nPress [Space] to begin the practice.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    confirm = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "practice_intro" ---
    prac_intro = visual.TextStim(win=win, name='prac_intro',
        text='This is the practice phase.\nAfter each response, you will receive feedback indicating whether your answer was correct or incorrect. This will help you familiarize yourself with the task.\nPress [Space] to begin the practice.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_2 = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "study_stage" ---
    # Run 'Begin Experiment' code from StudyCode
    import random
    import numpy as np
    from psychtoolbox import audio
    import sounddevice as sd
    sd.default.device = 'Headphones (Realtek(R) Audio)'
    Fix = visual.TextStim(win=win, name='Fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    stim1 = visual.Rect(
        win=win, name='stim1',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=1.0, depth=-2.0, interpolate=True)
    stim2 = visual.Rect(
        win=win, name='stim2',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    # set audio backend
    #sound.Sound.backend = 'ptb'
    audi1 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi1'
    )
    audi1.setVolume(1.0)
    audi2 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi2'
    )
    audi2.setVolume(1.0)
    # Using keyboard instead of Cedrus ResponseBox
    # Response keys: 'y' = Yes/Same, 'n' = No/Different

    # --- Initialize components for Routine "probe" ---
    # Run 'Begin Experiment' code from ProbeCode
    
    
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    targetV = visual.Rect(
        win=win, name='targetV',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetA = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='targetA'
    )
    targetA.setVolume(1.0)
    ResponseBox = keyboard.Keyboard(deviceName='ResponseBox')
    
    # --- Initialize components for Routine "feedback" ---
    answer = visual.TextStim(win=win, name='answer',
        text='',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    
    # --- Initialize components for Routine "SFT_start" ---
    text = visual.TextStim(win=win, name='text',
        text='You have completed the practice phase. The main experiment will now begin.\nThere will be a short break between each block.\nPress [Space] to start.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_3 = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "study_stage" ---
    # Run 'Begin Experiment' code from StudyCode
    import random
    import numpy as np
    from psychtoolbox import audio
    import sounddevice as sd
    sd.default.device = 'Headphones (Realtek(R) Audio)'
    Fix = visual.TextStim(win=win, name='Fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    stim1 = visual.Rect(
        win=win, name='stim1',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=1.0, depth=-2.0, interpolate=True)
    stim2 = visual.Rect(
        win=win, name='stim2',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    audi1 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi1'
    )
    audi1.setVolume(1.0)
    audi2 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi2'
    )
    audi2.setVolume(1.0)
    
    # --- Initialize components for Routine "probe" ---
    # Run 'Begin Experiment' code from ProbeCode
    
    
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='+',
        font='Arial',
         pos=(0, 0), draggable=False, height=.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    targetV = visual.Rect(
        win=win, name='targetV',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetA = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='targetA'
    )
    targetA.setVolume(1.0)
    ResponseBox = keyboard.Keyboard(deviceName='ResponseBox')
    
    # --- Initialize components for Routine "rest" ---
    timeout = visual.TextStim(win=win, name='timeout',
        text='Take a break. \nPress Space to continue.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    breakend = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "study_stage" ---
    # Run 'Begin Experiment' code from StudyCode
    import random
    import numpy as np
    from psychtoolbox import audio
    import sounddevice as sd
    sd.default.device = 'Headphones (Realtek(R) Audio)'
    Fix = visual.TextStim(win=win, name='Fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    stim1 = visual.Rect(
        win=win, name='stim1',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=1.0, depth=-2.0, interpolate=True)
    stim2 = visual.Rect(
        win=win, name='stim2',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    audi1 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi1'
    )
    audi1.setVolume(1.0)
    audi2 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi2'
    )
    audi2.setVolume(1.0)
    
    # --- Initialize components for Routine "probe" ---
    # Run 'Begin Experiment' code from ProbeCode
    
    
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='+',
        font='Arial',
         pos=(0, 0), draggable=False, height=.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    targetV = visual.Rect(
        win=win, name='targetV',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetA = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='targetA'
    )
    targetA.setVolume(1.0)
    ResponseBox = keyboard.Keyboard(deviceName='ResponseBox')
    
    # --- Initialize components for Routine "rest" ---
    timeout = visual.TextStim(win=win, name='timeout',
        text='Take a break. \nPress Space to continue.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    breakend = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "study_stage" ---
    # Run 'Begin Experiment' code from StudyCode
    import random
    import numpy as np
    from psychtoolbox import audio
    import sounddevice as sd
    sd.default.device = 'Headphones (Realtek(R) Audio)'
    Fix = visual.TextStim(win=win, name='Fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    stim1 = visual.Rect(
        win=win, name='stim1',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=1.0, depth=-2.0, interpolate=True)
    stim2 = visual.Rect(
        win=win, name='stim2',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    audi1 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi1'
    )
    audi1.setVolume(1.0)
    audi2 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi2'
    )
    audi2.setVolume(1.0)
    
    # --- Initialize components for Routine "probe" ---
    # Run 'Begin Experiment' code from ProbeCode
    
    
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='+',
        font='Arial',
         pos=(0, 0), draggable=False, height=.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    targetV = visual.Rect(
        win=win, name='targetV',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetA = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='targetA'
    )
    targetA.setVolume(1.0)
    ResponseBox = keyboard.Keyboard(deviceName='ResponseBox')
    
    # --- Initialize components for Routine "study_stage" ---
    # Run 'Begin Experiment' code from StudyCode
    import random
    import numpy as np
    from psychtoolbox import audio
    import sounddevice as sd
    sd.default.device = 'Headphones (Realtek(R) Audio)'
    Fix = visual.TextStim(win=win, name='Fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    stim1 = visual.Rect(
        win=win, name='stim1',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=1.0, depth=-2.0, interpolate=True)
    stim2 = visual.Rect(
        win=win, name='stim2',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    audi1 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi1'
    )
    audi1.setVolume(1.0)
    audi2 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi2'
    )
    audi2.setVolume(1.0)
    
    # --- Initialize components for Routine "probe" ---
    # Run 'Begin Experiment' code from ProbeCode
    
    
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    targetV = visual.Rect(
        win=win, name='targetV',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetA = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='targetA'
    )
    targetA.setVolume(1.0)
    ResponseBox = keyboard.Keyboard(deviceName='ResponseBox')
    
    # --- Initialize components for Routine "rest" ---
    timeout = visual.TextStim(win=win, name='timeout',
        text='Take a break. \nPress Space to continue.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    breakend = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "study_stage" ---
    # Run 'Begin Experiment' code from StudyCode
    import random
    import numpy as np
    from psychtoolbox import audio
    import sounddevice as sd
    sd.default.device = 'Headphones (Realtek(R) Audio)'
    Fix = visual.TextStim(win=win, name='Fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    stim1 = visual.Rect(
        win=win, name='stim1',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=1.0, depth=-2.0, interpolate=True)
    stim2 = visual.Rect(
        win=win, name='stim2',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    audi1 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi1'
    )
    audi1.setVolume(1.0)
    audi2 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi2'
    )
    audi2.setVolume(1.0)
    
    # --- Initialize components for Routine "probe" ---
    # Run 'Begin Experiment' code from ProbeCode
    
    
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='+',
        font='Arial', pos=(0, 0), draggable=False, height=.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    targetV = visual.Rect(
        win=win, name='targetV',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetA = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='targetA'
    )
    targetA.setVolume(1.0)
    ResponseBox = keyboard.Keyboard(deviceName='ResponseBox')
    
    # --- Initialize components for Routine "rest" ---
    timeout = visual.TextStim(win=win, name='timeout',
        text='Take a break. \nPress Space to continue.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    breakend = keyboard.Keyboard(deviceName='defaultKeyboard')
    
    # --- Initialize components for Routine "study_stage" ---
    # Run 'Begin Experiment' code from StudyCode
    import random
    import numpy as np
    from psychtoolbox import audio
    import sounddevice as sd
    sd.default.device = 'Headphones (Realtek(R) Audio)'
    Fix = visual.TextStim(win=win, name='Fix',
        text='+',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='named', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    stim1 = visual.Rect(
        win=win, name='stim1',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=1.0, depth=-2.0, interpolate=True)
    stim2 = visual.Rect(
        win=win, name='stim2',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-3.0, interpolate=True)
    audi1 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi1'
    )
    audi1.setVolume(1.0)
    audi2 = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='audi2'
    )
    audi2.setVolume(1.0)
    
    # --- Initialize components for Routine "probe" ---
    # Run 'Begin Experiment' code from ProbeCode
    
    
    Fixation = visual.TextStim(win=win, name='Fixation',
        text='+',
        font='Arial', pos=(0, 0), draggable=False, height=.2, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=1.0, 
        languageStyle='LTR',
        depth=-1.0);
    targetV = visual.Rect(
        win=win, name='targetV',units='pix', 
        width=(100,100)[0], height=(100,100)[1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='hex', lineColor='#808080', fillColor='white',
        opacity=None, depth=-2.0, interpolate=True)
    targetA = sound.Sound(
        'A', 
        secs=1, 
        stereo=True, 
        hamming=True, 
            name='targetA'
    )
    targetA.setVolume(1.0)
    ResponseBox = keyboard.Keyboard(deviceName='ResponseBox')
    
    # --- Initialize components for Routine "End" ---
    EndExp = visual.TextStim(win=win, name='EndExp',
        text='The experiment is finished. \nPlease find the experimenter.\nPress Space after you read this text.',
        font='Arial',
        pos=(0, 0), draggable=False, height=0.05, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    callExp = keyboard.Keyboard(deviceName='defaultKeyboard')
    
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
    
    # --- Prepare to start Routine "studyintro" ---
    # create an object to store info about Routine studyintro
    studyintro = data.Routine(
        name='studyintro',
        components=[intro, confirm],
    )
    studyintro.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for confirm
    confirm.keys = []
    confirm.rt = []
    _confirm_allKeys = []
    # store start times for studyintro
    studyintro.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    studyintro.tStart = globalClock.getTime(format='float')
    studyintro.status = STARTED
    thisExp.addData('studyintro.started', studyintro.tStart)
    studyintro.maxDuration = None
    # keep track of which components have finished
    studyintroComponents = studyintro.components
    for thisComponent in studyintro.components:
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
    
    # --- Run Routine "studyintro" ---
    thisExp.currentRoutine = studyintro
    studyintro.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *intro* updates
        
        # if intro is starting this frame...
        if intro.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            intro.frameNStart = frameN  # exact frame index
            intro.tStart = t  # local t and not account for scr refresh
            intro.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(intro, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'intro.started')
            # update status
            intro.status = STARTED
            intro.setAutoDraw(True)
        
        # if intro is active this frame...
        if intro.status == STARTED:
            # update params
            pass
        
        # *confirm* updates
        waitOnFlip = False
        
        # if confirm is starting this frame...
        if confirm.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            confirm.frameNStart = frameN  # exact frame index
            confirm.tStart = t  # local t and not account for scr refresh
            confirm.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(confirm, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'confirm.started')
            # update status
            confirm.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(confirm.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(confirm.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if confirm.status == STARTED and not waitOnFlip:
            theseKeys = confirm.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _confirm_allKeys.extend(theseKeys)
            if len(_confirm_allKeys):
                confirm.keys = _confirm_allKeys[-1].name  # just the last key pressed
                confirm.rt = _confirm_allKeys[-1].rt
                confirm.duration = _confirm_allKeys[-1].duration
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
                currentRoutine=studyintro,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            studyintro.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if studyintro.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in studyintro.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "studyintro" ---
    for thisComponent in studyintro.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for studyintro
    studyintro.tStop = globalClock.getTime(format='float')
    studyintro.tStopRefresh = tThisFlipGlobal
    thisExp.addData('studyintro.stopped', studyintro.tStop)
    # check responses
    if confirm.keys in ['', [], None]:  # No response was made
        confirm.keys = None
    thisExp.addData('confirm.keys',confirm.keys)
    if confirm.keys != None:  # we had a response
        thisExp.addData('confirm.rt', confirm.rt)
        thisExp.addData('confirm.duration', confirm.duration)
    thisExp.nextEntry()
    # the Routine "studyintro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "practice_intro" ---
    # create an object to store info about Routine practice_intro
    practice_intro = data.Routine(
        name='practice_intro',
        components=[prac_intro, key_resp_2],
    )
    practice_intro.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_2
    key_resp_2.keys = []
    key_resp_2.rt = []
    _key_resp_2_allKeys = []
    # store start times for practice_intro
    practice_intro.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    practice_intro.tStart = globalClock.getTime(format='float')
    practice_intro.status = STARTED
    thisExp.addData('practice_intro.started', practice_intro.tStart)
    practice_intro.maxDuration = None
    # keep track of which components have finished
    practice_introComponents = practice_intro.components
    for thisComponent in practice_intro.components:
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
    
    # --- Run Routine "practice_intro" ---
    thisExp.currentRoutine = practice_intro
    practice_intro.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *prac_intro* updates
        
        # if prac_intro is starting this frame...
        if prac_intro.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            prac_intro.frameNStart = frameN  # exact frame index
            prac_intro.tStart = t  # local t and not account for scr refresh
            prac_intro.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(prac_intro, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'prac_intro.started')
            # update status
            prac_intro.status = STARTED
            prac_intro.setAutoDraw(True)
        
        # if prac_intro is active this frame...
        if prac_intro.status == STARTED:
            # update params
            pass
        
        # prac_intro stays visible until space is pressed (no auto-stop)
        
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
            theseKeys = key_resp_2.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
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
                currentRoutine=practice_intro,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            practice_intro.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if practice_intro.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in practice_intro.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "practice_intro" ---
    for thisComponent in practice_intro.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for practice_intro
    practice_intro.tStop = globalClock.getTime(format='float')
    practice_intro.tStopRefresh = tThisFlipGlobal
    thisExp.addData('practice_intro.stopped', practice_intro.tStop)
    # check responses
    if key_resp_2.keys in ['', [], None]:  # No response was made
        key_resp_2.keys = None
    thisExp.addData('key_resp_2.keys',key_resp_2.keys)
    if key_resp_2.keys != None:  # we had a response
        thisExp.addData('key_resp_2.rt', key_resp_2.rt)
        thisExp.addData('key_resp_2.duration', key_resp_2.duration)
    thisExp.nextEntry()
    # the Routine "practice_intro" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    practice = data.TrialHandler2(
        name='practice',
        nReps=1,
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('stimuli/practice.csv'), 
        seed=None, 
        isTrials=True, 
    )
    thisExp.addLoop(practice)  # add the loop to the experiment
    thisPractice = practice.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisPractice.rgb)
    if thisPractice != None:
        for paramName in thisPractice:
            globals()[paramName] = thisPractice[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisPractice in practice:
        practice.status = STARTED
        if hasattr(thisPractice, 'status'):
            thisPractice.status = STARTED
        currentLoop = practice
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisPractice.rgb)
        if thisPractice != None:
            for paramName in thisPractice:
                globals()[paramName] = thisPractice[paramName]
        
        # --- Prepare to start Routine "study_stage" ---
        # create an object to store info about Routine study_stage
        study_stage = data.Routine(
            name='study_stage',
            components=[Fix, stim1, stim2, audi1, audi2],
        )
        study_stage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from StudyCode
        
        
        stim1.setFillColor(color1_target)
        stim1.setOpacity(1.0)
        stim1.setPos((-200, 0))
        stim2.setFillColor(color2_target)
        stim2.setOpacity(None)
        stim2.setPos((200,0))
        audi1.setSound(audio1_target_file, secs=1, hamming=True)
        audi1.setVolume(1.0, log=False)
        audi1.seek(0)
        audi2.setSound(audio2_target_file, secs=1, hamming=True)
        audi2.setVolume(1.0, log=False)
        audi2.seek(0)
        # store start times for study_stage
        study_stage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study_stage.tStart = globalClock.getTime(format='float')
        study_stage.status = STARTED
        thisExp.addData('study_stage.started', study_stage.tStart)
        study_stage.maxDuration = None
        # keep track of which components have finished
        study_stageComponents = study_stage.components
        for thisComponent in study_stage.components:
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
        
        # --- Run Routine "study_stage" ---
        thisExp.currentRoutine = study_stage
        study_stage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.3:
            # if trial has changed, end Routine now
            if hasattr(thisPractice, 'status') and thisPractice.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            
            # if Fix is starting this frame...
            if Fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fix.frameNStart = frameN  # exact frame index
                Fix.tStart = t  # local t and not account for scr refresh
                Fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fix.started')
                # update status
                Fix.status = STARTED
                Fix.setAutoDraw(True)
            
            # if Fix is active this frame...
            if Fix.status == STARTED:
                # update params
                pass
            
            # if Fix is stopping this frame...
            if Fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fix.tStartRefresh + .3-frameTolerance:
                    # keep track of stop time/frame for later
                    Fix.tStop = t  # not accounting for scr refresh
                    Fix.tStopRefresh = tThisFlipGlobal  # on global time
                    Fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fix.stopped')
                    # update status
                    Fix.status = FINISHED
                    Fix.setAutoDraw(False)
            
            # *stim1* updates
            
            # if stim1 is starting this frame...
            if stim1.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                # keep track of start time/frame for later
                stim1.frameNStart = frameN  # exact frame index
                stim1.tStart = t  # local t and not account for scr refresh
                stim1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim1.started')
                # update status
                stim1.status = STARTED
                stim1.setAutoDraw(True)
            
            # if stim1 is active this frame...
            if stim1.status == STARTED:
                # update params
                pass
            
            # if stim1 is stopping this frame...
            if stim1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim1.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim1.tStop = t  # not accounting for scr refresh
                    stim1.tStopRefresh = tThisFlipGlobal  # on global time
                    stim1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim1.stopped')
                    # update status
                    stim1.status = FINISHED
                    stim1.setAutoDraw(False)
            
            # *stim2* updates
            
            # if stim2 is starting this frame...
            if stim2.status == NOT_STARTED and tThisFlip >= 1.3-frameTolerance:
                # keep track of start time/frame for later
                stim2.frameNStart = frameN  # exact frame index
                stim2.tStart = t  # local t and not account for scr refresh
                stim2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim2.started')
                # update status
                stim2.status = STARTED
                stim2.setAutoDraw(True)
            
            # if stim2 is active this frame...
            if stim2.status == STARTED:
                # update params
                pass
            
            # if stim2 is stopping this frame...
            if stim2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim2.tStop = t  # not accounting for scr refresh
                    stim2.tStopRefresh = tThisFlipGlobal  # on global time
                    stim2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim2.stopped')
                    # update status
                    stim2.status = FINISHED
                    stim2.setAutoDraw(False)
            
            # *audi1* updates
            
            # if audi1 is starting this frame...
            if audi1.status == NOT_STARTED and tThisFlip >= 2.3-frameTolerance:
                # keep track of start time/frame for later
                audi1.frameNStart = frameN  # exact frame index
                audi1.tStart = t  # local t and not account for scr refresh
                audi1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi1.started', tThisFlipGlobal)
                # update status
                audi1.status = STARTED
                audi1.play(when=win)  # sync with win flip
            
            # if audi1 is stopping this frame...
            if audi1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi1.tStartRefresh + 1-frameTolerance or audi1.isFinished:
                    # keep track of stop time/frame for later
                    audi1.tStop = t  # not accounting for scr refresh
                    audi1.tStopRefresh = tThisFlipGlobal  # on global time
                    audi1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi1.stopped')
                    # update status
                    audi1.status = FINISHED
                    audi1.stop()
            
            # *audi2* updates
            
            # if audi2 is starting this frame...
            if audi2.status == NOT_STARTED and tThisFlip >= 3.3-frameTolerance:
                # keep track of start time/frame for later
                audi2.frameNStart = frameN  # exact frame index
                audi2.tStart = t  # local t and not account for scr refresh
                audi2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi2.started', tThisFlipGlobal)
                # update status
                audi2.status = STARTED
                audi2.play(when=win)  # sync with win flip
            
            # if audi2 is stopping this frame...
            if audi2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi2.tStartRefresh + 1-frameTolerance or audi2.isFinished:
                    # keep track of stop time/frame for later
                    audi2.tStop = t  # not accounting for scr refresh
                    audi2.tStopRefresh = tThisFlipGlobal  # on global time
                    audi2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi2.stopped')
                    # update status
                    audi2.status = FINISHED
                    audi2.stop()
            
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
                    currentRoutine=study_stage,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study_stage.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study_stage.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study_stage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study_stage" ---
        for thisComponent in study_stage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study_stage
        study_stage.tStop = globalClock.getTime(format='float')
        study_stage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study_stage.stopped', study_stage.tStop)
        audi1.pause()  # ensure sound has stopped at end of Routine
        audi2.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if study_stage.maxDurationReached:
            routineTimer.addTime(-study_stage.maxDuration)
        elif study_stage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.300000)

        # Generate stratified conditions for 9 probe trials
        probe_conditions = generate_stratified_conditions()
        probe_idx = 0

        # set up handler to look after randomisation of conditions etc
        inner = data.TrialHandler2(
            name='inner',
            nReps=9,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=[None],
            seed=None,
            isTrials=True,
        )
        thisExp.addLoop(inner)  # add the loop to the experiment
        thisInner = inner.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisInner.rgb)
        if thisInner != None:
            for paramName in thisInner:
                globals()[paramName] = thisInner[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()

        for thisInner in inner:
            inner.status = STARTED
            if hasattr(thisInner, 'status'):
                thisInner.status = STARTED
            currentLoop = inner
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisInner.rgb)
            if thisInner != None:
                for paramName in thisInner:
                    globals()[paramName] = thisInner[paramName]

            # --- Prepare to start Routine "probe" ---
            # create an object to store info about Routine probe
            probe = data.Routine(
                name='probe',
                components=[Fixation, targetV, targetA, ResponseBox],
            )
            probe.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from ProbeCode
            # Use pre-generated stratified condition
            condition = probe_conditions[probe_idx]
            probe_idx += 1
            #AX AX= color, XA= audio
            #AA=0,1  HA=2,3  LA=4,5  AH=6,7
            #HH=8,9  LH=10,11  AL=12,13  HL=14,15  LL=16,17
            if condition == 0:  # AA
               targetCol = color1_target
               targetAud = audio1_target_file
            elif condition == 1:#AA.25
                targetCol = color2_target
                targetAud = audio2_target_file
            if condition == 2:#HA
               targetCol = color1_target
               targetAud = audio1_H_file
            elif condition == 3:#HA
                targetCol = color2_target
                targetAud = audio2_H_file
            if condition == 4:#LA
               targetCol = color1_target
               targetAud = audio1_L_file
            elif condition == 5:#LA
                targetCol = color2_target
                targetAud = audio2_L_file
            if condition == 6:#AH
               targetCol = color1_H
               targetAud = audio1_target_file
            elif condition == 7:#AH
                targetCol = color2_H
                targetAud = audio2_target_file
            if condition == 8:#HH
               targetCol = color1_H
               targetAud = audio1_H_file
            elif condition == 9:#HH
                targetCol = color2_H
                targetAud = audio2_H_file
            if condition == 10:#LH
               targetCol = color1_L
               targetAud = audio1_H_file
            elif condition == 11:#LH
                targetCol = color2_L
                targetAud = audio2_H_file
            if condition == 12: #AL
               targetCol = color1_L
               targetAud = audio1_target_file
            elif condition == 13: #AL
                targetCol = color2_L
                targetAud = audio2_target_file
            if condition == 14:#HL
               targetCol = color1_H
               targetAud = audio1_L_file
            elif condition == 15:#HL
                targetCol = color2_H
                targetAud = audio2_L_file
            if condition == 16:#LL
               targetCol = color1_L
               targetAud = audio1_L_file
            elif condition == 17:#LL
                targetCol = color2_L
                targetAud = audio2_L_file
            
            targetV.setFillColor(targetCol)
            targetV.setPos((0,0))
            targetA.setSound(targetAud, secs=1, hamming=True)
            targetA.setVolume(1.0, log=False)
            targetA.seek(0)
            ResponseBox.keys = []  # to store response values
            ResponseBox.rt = []
            ResponseBox.status = NOT_STARTED
            # store start times for probe
            probe.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            probe.tStart = globalClock.getTime(format='float')
            probe.status = STARTED
            thisExp.addData('probe.started', probe.tStart)
            probe.maxDuration = None
            # keep track of which components have finished
            probeComponents = probe.components
            for thisComponent in probe.components:
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
            
            # --- Run Routine "probe" ---
            thisExp.currentRoutine = probe
            probe.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 3.3:
                # if trial has changed, end Routine now
                if hasattr(thisInner, 'status') and thisInner.status == STOPPING:
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
                    if tThisFlipGlobal > Fixation.tStartRefresh + .3-frameTolerance:
                        # keep track of stop time/frame for later
                        Fixation.tStop = t  # not accounting for scr refresh
                        Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        Fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Fixation.stopped')
                        # update status
                        Fixation.status = FINISHED
                        Fixation.setAutoDraw(False)
                
                # *targetV* updates
                
                # if targetV is starting this frame...
                if targetV.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetV.frameNStart = frameN  # exact frame index
                    targetV.tStart = t  # local t and not account for scr refresh
                    targetV.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(targetV, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetV.started')
                    # update status
                    targetV.status = STARTED
                    targetV.setAutoDraw(True)
                
                # if targetV is active this frame...
                if targetV.status == STARTED:
                    # update params
                    pass
                
                # if targetV is stopping this frame...
                if targetV.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetV.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        targetV.tStop = t  # not accounting for scr refresh
                        targetV.tStopRefresh = tThisFlipGlobal  # on global time
                        targetV.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetV.stopped')
                        # update status
                        targetV.status = FINISHED
                        targetV.setAutoDraw(False)
                
                # *targetA* updates
                
                # if targetA is starting this frame...
                if targetA.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetA.frameNStart = frameN  # exact frame index
                    targetA.tStart = t  # local t and not account for scr refresh
                    targetA.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('targetA.started', tThisFlipGlobal)
                    # update status
                    targetA.status = STARTED
                    targetA.play(when=win)  # sync with win flip
                
                # if targetA is stopping this frame...
                if targetA.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetA.tStartRefresh + 1-frameTolerance or targetA.isFinished:
                        # keep track of stop time/frame for later
                        targetA.tStop = t  # not accounting for scr refresh
                        targetA.tStopRefresh = tThisFlipGlobal  # on global time
                        targetA.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetA.stopped')
                        # update status
                        targetA.status = FINISHED
                        targetA.stop()
                # *ResponseBox* updates
                
                # if ResponseBox is starting this frame...
                if ResponseBox.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    ResponseBox.frameNStart = frameN  # exact frame index
                    ResponseBox.tStart = t  # local t and not account for scr refresh
                    ResponseBox.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ResponseBox, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    ResponseBox.status = STARTED
                    ResponseBox.clock.reset()  # now t=0
                    # clear keyboard responses
                    ResponseBox.keys = []
                    ResponseBox.rt = []
                    ResponseBox.clearEvents(eventType='keyboard')
                
                # if ResponseBox is stopping this frame...
                if ResponseBox.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ResponseBox.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        ResponseBox.tStop = t  # not accounting for scr refresh
                        ResponseBox.tStopRefresh = tThisFlipGlobal  # on global time
                        ResponseBox.frameNStop = frameN  # exact frame index
                        # update status
                        ResponseBox.status = FINISHED
                if ResponseBox.status == STARTED:
                    # check for key presses using keyboard
                    theseKeys = ResponseBox.getKeys(keyList=['y', 'n'], ignoreKeys=["escape"], waitRelease=False)
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if ResponseBox.keys == []:  # then this is first keypress
                            ResponseBox.keys = theseKeys[0].name  # 'y' or 'n'
                            ResponseBox.rt = theseKeys[0].rt
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
                        currentRoutine=probe,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    probe.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if probe.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in probe.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "probe" ---
            for thisComponent in probe.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for probe
            probe.tStop = globalClock.getTime(format='float')
            probe.tStopRefresh = tThisFlipGlobal
            thisExp.addData('probe.stopped', probe.tStop)
            # Run 'End Routine' code from ProbeCode
            # Check if the hardware was actually found and a response was made
            #if ResponseBox is not None and hasattr(ResponseBox, 'duration'):
            #    if ResponseBox.duration is not None:
            #        thisExp.addData('ResponseBox.duration', ResponseBox.duration)
            # Check if the hardware was initialized and a response occurred
            if ResponseBox is not None:
                # Use getattr to safely check for 'duration' without crashing
                resp_dur = getattr(ResponseBox, 'duration', None)
                if resp_dur is not None:
                    thisExp.addData('ResponseBox.duration', resp_dur)
                else:
                    thisExp.addData('ResponseBox.duration', 'no_response')
            else:
                thisExp.addData('ResponseBox.duration', 'device_not_found')
            thisExp.addData('condition', condition)
            thisExp.addData('TargetA', targetAud)
            thisExp.addData('TargetC', targetCol)
            
            targetA.pause()  # ensure sound has stopped at end of Routine
            # check responses
            if ResponseBox.keys in ['', [], None]:  # No response was made
                ResponseBox.keys = None
            inner.addData('ResponseBox.keys',ResponseBox.keys)
            if ResponseBox.keys != None:  # we had a response
                inner.addData('ResponseBox.rt', ResponseBox.rt)
                #inner.addData('ResponseBox.duration', ResponseBox.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if probe.maxDurationReached:
                routineTimer.addTime(-probe.maxDuration)
            elif probe.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-3.300000)
            
            # --- Prepare to start Routine "feedback" ---
            # create an object to store info about Routine feedback
            feedback = data.Routine(
                name='feedback',
                components=[answer],
            )
            feedback.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from code
            # Use rule.csv to determine correct answer based on probe types
            trial_data = {
                'color1_target': color1_target, 'color2_target': color2_target,
                'color1_H': color1_H, 'color1_L': color1_L,
                'color2_H': color2_H, 'color2_L': color2_L,
                'audio1_target_file': audio1_target_file, 'audio2_target_file': audio2_target_file,
                'audio1_H_file': audio1_H_file, 'audio1_L_file': audio1_L_file,
                'audio2_H_file': audio2_H_file, 'audio2_L_file': audio2_L_file,
            }
            col_type, aud_type = get_probe_types(targetCol, targetAud, trial_data)

            # Look up rule based on (col_type, aud_type, response)
            # rule.csv 的 ResponseBox 欄是 Cedrus 按鍵碼：4 = Yes/相同、3 = No/不同（rule.csv 第 2、4 列）；
            # 鍵盤版收到的是 'y' / 'n'，要先換成按鍵碼，否則 rule_key 永遠對不上、acc 恆為 0。
            user_response = {'y': '4', 'n': '3'}.get(ResponseBox.keys, 'None') if ResponseBox.keys else 'None'
            rule_key = (col_type, aud_type, user_response)
            if rule_key in FEEDBACK_RULES:
                acc = FEEDBACK_RULES[rule_key]['Acc']
                resp = FEEDBACK_RULES[rule_key]['resp']
            else:
                # Fallback: no response or unknown combination
                acc = 0
                resp = "Incorrect"
            answer.setText(resp)
            # store start times for feedback
            feedback.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            feedback.tStart = globalClock.getTime(format='float')
            feedback.status = STARTED
            thisExp.addData('feedback.started', feedback.tStart)
            feedback.maxDuration = None
            # keep track of which components have finished
            feedbackComponents = feedback.components
            for thisComponent in feedback.components:
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
            
            # --- Run Routine "feedback" ---
            thisExp.currentRoutine = feedback
            feedback.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 1.0:
                # if trial has changed, end Routine now
                if hasattr(thisInner, 'status') and thisInner.status == STOPPING:
                    continueRoutine = False
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *answer* updates
                
                # if answer is starting this frame...
                if answer.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    answer.frameNStart = frameN  # exact frame index
                    answer.tStart = t  # local t and not account for scr refresh
                    answer.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(answer, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'answer.started')
                    # update status
                    answer.status = STARTED
                    answer.setAutoDraw(True)
                
                # if answer is active this frame...
                if answer.status == STARTED:
                    # update params
                    pass
                
                # if answer is stopping this frame...
                if answer.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > answer.tStartRefresh + 1.0-frameTolerance:
                        # keep track of stop time/frame for later
                        answer.tStop = t  # not accounting for scr refresh
                        answer.tStopRefresh = tThisFlipGlobal  # on global time
                        answer.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'answer.stopped')
                        # update status
                        answer.status = FINISHED
                        answer.setAutoDraw(False)
                
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
                        currentRoutine=feedback,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    feedback.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if feedback.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in feedback.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "feedback" ---
            for thisComponent in feedback.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for feedback
            feedback.tStop = globalClock.getTime(format='float')
            feedback.tStopRefresh = tThisFlipGlobal
            thisExp.addData('feedback.stopped', feedback.tStop)
            # Run 'End Routine' code from code
            # Store accuracy (already calculated using rule.csv in Begin Routine)
            thisExp.addData("Acc", acc)
            thisExp.addData("col_type", col_type)
            thisExp.addData("aud_type", aud_type)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if feedback.maxDurationReached:
                routineTimer.addTime(-feedback.maxDuration)
            elif feedback.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-1.000000)
            # mark thisInner as finished
            if hasattr(thisInner, 'status'):
                thisInner.status = FINISHED
            # if awaiting a pause, pause now
            if inner.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                inner.status = STARTED
            thisExp.nextEntry()
            
        # completed 9 repeats of 'inner'
        inner.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisPractice as finished
        if hasattr(thisPractice, 'status'):
            thisPractice.status = FINISHED
        # if awaiting a pause, pause now
        if practice.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            practice.status = STARTED
        thisExp.nextEntry()
        
    # completed 5 repeats of 'practice'
    practice.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "SFT_start" ---
    # create an object to store info about Routine SFT_start
    SFT_start = data.Routine(
        name='SFT_start',
        components=[text, key_resp_3],
    )
    SFT_start.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_3
    key_resp_3.keys = []
    key_resp_3.rt = []
    _key_resp_3_allKeys = []
    # store start times for SFT_start
    SFT_start.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    SFT_start.tStart = globalClock.getTime(format='float')
    SFT_start.status = STARTED
    thisExp.addData('SFT_start.started', SFT_start.tStart)
    SFT_start.maxDuration = None
    # keep track of which components have finished
    SFT_startComponents = SFT_start.components
    for thisComponent in SFT_start.components:
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
    
    # --- Run Routine "SFT_start" ---
    thisExp.currentRoutine = SFT_start
    SFT_start.forceEnded = routineForceEnded = not continueRoutine
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
        
        # text stays visible until space is pressed (no auto-stop)

        # *key_resp_3* updates
        waitOnFlip = False
        
        # if key_resp_3 is starting this frame...
        if key_resp_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.tStart = t  # local t and not account for scr refresh
            key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_3.started')
            # update status
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_3.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_3.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _key_resp_3_allKeys.extend(theseKeys)
            if len(_key_resp_3_allKeys):
                key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                key_resp_3.duration = _key_resp_3_allKeys[-1].duration
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
                currentRoutine=SFT_start,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            SFT_start.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if SFT_start.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in SFT_start.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "SFT_start" ---
    for thisComponent in SFT_start.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for SFT_start
    SFT_start.tStop = globalClock.getTime(format='float')
    SFT_start.tStopRefresh = tThisFlipGlobal
    thisExp.addData('SFT_start.stopped', SFT_start.tStop)
    # check responses
    if key_resp_3.keys in ['', [], None]:  # No response was made
        key_resp_3.keys = None
    thisExp.addData('key_resp_3.keys',key_resp_3.keys)
    if key_resp_3.keys != None:  # we had a response
        thisExp.addData('key_resp_3.rt', key_resp_3.rt)
        thisExp.addData('key_resp_3.duration', key_resp_3.duration)
    thisExp.nextEntry()
    # the Routine "SFT_start" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    block1 = data.TrialHandler2(
        name='block1',
        nReps=1,
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('stimuli/block1.csv'), 
        seed=45, 
        isTrials=True, 
    )
    thisExp.addLoop(block1)  # add the loop to the experiment
    thisBlock1 = block1.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
    if thisBlock1 != None:
        for paramName in thisBlock1:
            globals()[paramName] = thisBlock1[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock1 in block1:
        block1.status = STARTED
        if hasattr(thisBlock1, 'status'):
            thisBlock1.status = STARTED
        currentLoop = block1
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock1.rgb)
        if thisBlock1 != None:
            for paramName in thisBlock1:
                globals()[paramName] = thisBlock1[paramName]
        
        # --- Prepare to start Routine "study_stage" ---
        # create an object to store info about Routine study_stage
        study_stage = data.Routine(
            name='study_stage',
            components=[Fix, stim1, stim2, audi1, audi2],
        )
        study_stage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from StudyCode
        
        
        stim1.setFillColor(color1_target)
        stim1.setOpacity(1.0)
        stim1.setPos((-200, 0))
        stim2.setFillColor(color2_target)
        stim2.setOpacity(None)
        stim2.setPos((200,0))
        audi1.setSound(audio1_target_file, secs=1, hamming=True)
        audi1.setVolume(1.0, log=False)
        audi1.seek(0)
        audi2.setSound(audio2_target_file, secs=1, hamming=True)
        audi2.setVolume(1.0, log=False)
        audi2.seek(0)
        # store start times for study_stage
        study_stage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study_stage.tStart = globalClock.getTime(format='float')
        study_stage.status = STARTED
        thisExp.addData('study_stage.started', study_stage.tStart)
        study_stage.maxDuration = None
        # keep track of which components have finished
        study_stageComponents = study_stage.components
        for thisComponent in study_stage.components:
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
        
        # --- Run Routine "study_stage" ---
        thisExp.currentRoutine = study_stage
        study_stage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.3:
            # if trial has changed, end Routine now
            if hasattr(thisBlock1, 'status') and thisBlock1.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            
            # if Fix is starting this frame...
            if Fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fix.frameNStart = frameN  # exact frame index
                Fix.tStart = t  # local t and not account for scr refresh
                Fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fix.started')
                # update status
                Fix.status = STARTED
                Fix.setAutoDraw(True)
            
            # if Fix is active this frame...
            if Fix.status == STARTED:
                # update params
                pass
            
            # if Fix is stopping this frame...
            if Fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fix.tStartRefresh + .3-frameTolerance:
                    # keep track of stop time/frame for later
                    Fix.tStop = t  # not accounting for scr refresh
                    Fix.tStopRefresh = tThisFlipGlobal  # on global time
                    Fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fix.stopped')
                    # update status
                    Fix.status = FINISHED
                    Fix.setAutoDraw(False)
            
            # *stim1* updates
            
            # if stim1 is starting this frame...
            if stim1.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                # keep track of start time/frame for later
                stim1.frameNStart = frameN  # exact frame index
                stim1.tStart = t  # local t and not account for scr refresh
                stim1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim1.started')
                # update status
                stim1.status = STARTED
                stim1.setAutoDraw(True)
            
            # if stim1 is active this frame...
            if stim1.status == STARTED:
                # update params
                pass
            
            # if stim1 is stopping this frame...
            if stim1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim1.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim1.tStop = t  # not accounting for scr refresh
                    stim1.tStopRefresh = tThisFlipGlobal  # on global time
                    stim1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim1.stopped')
                    # update status
                    stim1.status = FINISHED
                    stim1.setAutoDraw(False)
            
            # *stim2* updates
            
            # if stim2 is starting this frame...
            if stim2.status == NOT_STARTED and tThisFlip >= 1.3-frameTolerance:
                # keep track of start time/frame for later
                stim2.frameNStart = frameN  # exact frame index
                stim2.tStart = t  # local t and not account for scr refresh
                stim2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim2.started')
                # update status
                stim2.status = STARTED
                stim2.setAutoDraw(True)
            
            # if stim2 is active this frame...
            if stim2.status == STARTED:
                # update params
                pass
            
            # if stim2 is stopping this frame...
            if stim2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim2.tStop = t  # not accounting for scr refresh
                    stim2.tStopRefresh = tThisFlipGlobal  # on global time
                    stim2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim2.stopped')
                    # update status
                    stim2.status = FINISHED
                    stim2.setAutoDraw(False)
            
            # *audi1* updates
            
            # if audi1 is starting this frame...
            if audi1.status == NOT_STARTED and tThisFlip >= 2.3-frameTolerance:
                # keep track of start time/frame for later
                audi1.frameNStart = frameN  # exact frame index
                audi1.tStart = t  # local t and not account for scr refresh
                audi1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi1.started', tThisFlipGlobal)
                # update status
                audi1.status = STARTED
                audi1.play(when=win)  # sync with win flip
            
            # if audi1 is stopping this frame...
            if audi1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi1.tStartRefresh + 1-frameTolerance or audi1.isFinished:
                    # keep track of stop time/frame for later
                    audi1.tStop = t  # not accounting for scr refresh
                    audi1.tStopRefresh = tThisFlipGlobal  # on global time
                    audi1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi1.stopped')
                    # update status
                    audi1.status = FINISHED
                    audi1.stop()
            
            # *audi2* updates
            
            # if audi2 is starting this frame...
            if audi2.status == NOT_STARTED and tThisFlip >= 3.3-frameTolerance:
                # keep track of start time/frame for later
                audi2.frameNStart = frameN  # exact frame index
                audi2.tStart = t  # local t and not account for scr refresh
                audi2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi2.started', tThisFlipGlobal)
                # update status
                audi2.status = STARTED
                audi2.play(when=win)  # sync with win flip
            
            # if audi2 is stopping this frame...
            if audi2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi2.tStartRefresh + 1-frameTolerance or audi2.isFinished:
                    # keep track of stop time/frame for later
                    audi2.tStop = t  # not accounting for scr refresh
                    audi2.tStopRefresh = tThisFlipGlobal  # on global time
                    audi2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi2.stopped')
                    # update status
                    audi2.status = FINISHED
                    audi2.stop()
            
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
                    currentRoutine=study_stage,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study_stage.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study_stage.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study_stage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study_stage" ---
        for thisComponent in study_stage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study_stage
        study_stage.tStop = globalClock.getTime(format='float')
        study_stage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study_stage.stopped', study_stage.tStop)
        audi1.pause()  # ensure sound has stopped at end of Routine
        audi2.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if study_stage.maxDurationReached:
            routineTimer.addTime(-study_stage.maxDuration)
        elif study_stage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.300000)

        # Generate stratified conditions for 9 probe trials
        probe_conditions = generate_stratified_conditions()
        probe_idx = 0

        # set up handler to look after randomisation of conditions etc
        SFT1 = data.TrialHandler2(
            name='SFT1',
            nReps=9,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=[None],
            seed=None,
            isTrials=True,
        )
        thisExp.addLoop(SFT1)  # add the loop to the experiment
        thisSFT1 = SFT1.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSFT1.rgb)
        if thisSFT1 != None:
            for paramName in thisSFT1:
                globals()[paramName] = thisSFT1[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisSFT1 in SFT1:
            SFT1.status = STARTED
            if hasattr(thisSFT1, 'status'):
                thisSFT1.status = STARTED
            currentLoop = SFT1
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisSFT1.rgb)
            if thisSFT1 != None:
                for paramName in thisSFT1:
                    globals()[paramName] = thisSFT1[paramName]

            # --- Prepare to start Routine "probe" ---
            # create an object to store info about Routine probe
            probe = data.Routine(
                name='probe',
                components=[Fixation, targetV, targetA, ResponseBox],
            )
            probe.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from ProbeCode
            # Use pre-generated stratified condition
            condition = probe_conditions[probe_idx]
            probe_idx += 1
            #AX AX= color, XA= audio
            #AA=0,1  HA=2,3  LA=4,5  AH=6,7
            #HH=8,9  LH=10,11  AL=12,13  HL=14,15  LL=16,17
            if condition == 0:  # AA
               targetCol = color1_target
               targetAud = audio1_target_file
            elif condition == 1:#AA.25
                targetCol = color2_target
                targetAud = audio2_target_file
            if condition == 2:#HA
               targetCol = color1_target
               targetAud = audio1_H_file
            elif condition == 3:#HA
                targetCol = color2_target
                targetAud = audio2_H_file
            if condition == 4:#LA
               targetCol = color1_target
               targetAud = audio1_L_file
            elif condition == 5:#LA
                targetCol = color2_target
                targetAud = audio2_L_file
            if condition == 6:#AH
               targetCol = color1_H
               targetAud = audio1_target_file
            elif condition == 7:#AH
                targetCol = color2_H
                targetAud = audio2_target_file
            if condition == 8:#HH
               targetCol = color1_H
               targetAud = audio1_H_file
            elif condition == 9:#HH
                targetCol = color2_H
                targetAud = audio2_H_file
            if condition == 10:#LH
               targetCol = color1_L
               targetAud = audio1_H_file
            elif condition == 11:#LH
                targetCol = color2_L
                targetAud = audio2_H_file
            if condition == 12: #AL
               targetCol = color1_L
               targetAud = audio1_target_file
            elif condition == 13: #AL
                targetCol = color2_L
                targetAud = audio2_target_file
            if condition == 14:#HL
               targetCol = color1_H
               targetAud = audio1_L_file
            elif condition == 15:#HL
                targetCol = color2_H
                targetAud = audio2_L_file
            if condition == 16:#LL
               targetCol = color1_L
               targetAud = audio1_L_file
            elif condition == 17:#LL
                targetCol = color2_L
                targetAud = audio2_L_file
            
            targetV.setFillColor(targetCol)
            targetV.setPos((0,0))
            targetA.setSound(targetAud, secs=1, hamming=True)
            targetA.setVolume(1.0, log=False)
            targetA.seek(0)
            ResponseBox.keys = []  # to store response values
            ResponseBox.rt = []
            ResponseBox.status = NOT_STARTED
            # store start times for probe
            probe.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            probe.tStart = globalClock.getTime(format='float')
            probe.status = STARTED
            thisExp.addData('probe.started', probe.tStart)
            probe.maxDuration = None
            # keep track of which components have finished
            probeComponents = probe.components
            for thisComponent in probe.components:
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
            
            # --- Run Routine "probe" ---
            thisExp.currentRoutine = probe
            probe.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 3.3:
                # if trial has changed, end Routine now
                if hasattr(thisSFT1, 'status') and thisSFT1.status == STOPPING:
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
                    if tThisFlipGlobal > Fixation.tStartRefresh + .3-frameTolerance:
                        # keep track of stop time/frame for later
                        Fixation.tStop = t  # not accounting for scr refresh
                        Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        Fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Fixation.stopped')
                        # update status
                        Fixation.status = FINISHED
                        Fixation.setAutoDraw(False)
                
                # *targetV* updates
                
                # if targetV is starting this frame...
                if targetV.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetV.frameNStart = frameN  # exact frame index
                    targetV.tStart = t  # local t and not account for scr refresh
                    targetV.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(targetV, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetV.started')
                    # update status
                    targetV.status = STARTED
                    targetV.setAutoDraw(True)
                
                # if targetV is active this frame...
                if targetV.status == STARTED:
                    # update params
                    pass
                
                # if targetV is stopping this frame...
                if targetV.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetV.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        targetV.tStop = t  # not accounting for scr refresh
                        targetV.tStopRefresh = tThisFlipGlobal  # on global time
                        targetV.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetV.stopped')
                        # update status
                        targetV.status = FINISHED
                        targetV.setAutoDraw(False)
                
                # *targetA* updates
                
                # if targetA is starting this frame...
                if targetA.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetA.frameNStart = frameN  # exact frame index
                    targetA.tStart = t  # local t and not account for scr refresh
                    targetA.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('targetA.started', tThisFlipGlobal)
                    # update status
                    targetA.status = STARTED
                    targetA.play(when=win)  # sync with win flip
                
                # if targetA is stopping this frame...
                if targetA.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetA.tStartRefresh + 1-frameTolerance or targetA.isFinished:
                        # keep track of stop time/frame for later
                        targetA.tStop = t  # not accounting for scr refresh
                        targetA.tStopRefresh = tThisFlipGlobal  # on global time
                        targetA.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetA.stopped')
                        # update status
                        targetA.status = FINISHED
                        targetA.stop()
                # *ResponseBox* updates
                
                # if ResponseBox is starting this frame...
                if ResponseBox.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    ResponseBox.frameNStart = frameN  # exact frame index
                    ResponseBox.tStart = t  # local t and not account for scr refresh
                    ResponseBox.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ResponseBox, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    ResponseBox.status = STARTED
                    ResponseBox.clock.reset()  # now t=0
                    # clear keyboard responses
                    ResponseBox.keys = []
                    ResponseBox.rt = []
                    ResponseBox.clearEvents(eventType='keyboard')
                
                # if ResponseBox is stopping this frame...
                if ResponseBox.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ResponseBox.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        ResponseBox.tStop = t  # not accounting for scr refresh
                        ResponseBox.tStopRefresh = tThisFlipGlobal  # on global time
                        ResponseBox.frameNStop = frameN  # exact frame index
                        # update status
                        ResponseBox.status = FINISHED
                if ResponseBox.status == STARTED:
                    # check for key presses using keyboard
                    theseKeys = ResponseBox.getKeys(keyList=['y', 'n'], ignoreKeys=["escape"], waitRelease=False)
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if ResponseBox.keys == []:  # then this is first keypress
                            ResponseBox.keys = theseKeys[0].name  # 'y' or 'n'
                            ResponseBox.rt = theseKeys[0].rt
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
                        currentRoutine=probe,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    probe.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if probe.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in probe.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "probe" ---
            for thisComponent in probe.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for probe
            probe.tStop = globalClock.getTime(format='float')
            probe.tStopRefresh = tThisFlipGlobal
            thisExp.addData('probe.stopped', probe.tStop)
            # Run 'End Routine' code from ProbeCode
            # Check if the hardware was actually found and a response was made
            #if ResponseBox is not None and hasattr(ResponseBox, 'duration'):
            #    if ResponseBox.duration is not None:
            #        thisExp.addData('ResponseBox.duration', ResponseBox.duration)
            # Check if the hardware was initialized and a response occurred
            if ResponseBox is not None:
                # Use getattr to safely check for 'duration' without crashing
                resp_dur = getattr(ResponseBox, 'duration', None)
                if resp_dur is not None:
                    thisExp.addData('ResponseBox.duration', resp_dur)
                else:
                    thisExp.addData('ResponseBox.duration', 'no_response')
            else:
                thisExp.addData('ResponseBox.duration', 'device_not_found')
            thisExp.addData('condition', condition)
            thisExp.addData('TargetA', targetAud)
            thisExp.addData('TargetC', targetCol)
            
            targetA.pause()  # ensure sound has stopped at end of Routine
            # check responses
            if ResponseBox.keys in ['', [], None]:  # No response was made
                ResponseBox.keys = None
            SFT1.addData('ResponseBox.keys',ResponseBox.keys)
            if ResponseBox.keys != None:  # we had a response
                SFT1.addData('ResponseBox.rt', ResponseBox.rt)
            #    SFT1.addData('ResponseBox.duration', ResponseBox.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if probe.maxDurationReached:
                routineTimer.addTime(-probe.maxDuration)
            elif probe.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-3.300000)
            # mark thisSFT1 as finished
            if hasattr(thisSFT1, 'status'):
                thisSFT1.status = FINISHED
            # if awaiting a pause, pause now
            if SFT1.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                SFT1.status = STARTED
            thisExp.nextEntry()
            
        # completed 32 repeats of 'SFT1'
        SFT1.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisBlock1 as finished
        if hasattr(thisBlock1, 'status'):
            thisBlock1.status = FINISHED
        # if awaiting a pause, pause now
        if block1.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            block1.status = STARTED
        thisExp.nextEntry()
        
    # completed 25 repeats of 'block1'
    block1.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "rest" ---
    # create an object to store info about Routine rest
    rest = data.Routine(
        name='rest',
        components=[timeout, breakend],
    )
    rest.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for breakend
    breakend.keys = []
    breakend.rt = []
    _breakend_allKeys = []
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
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *timeout* updates
        
        # if timeout is starting this frame...
        if timeout.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            timeout.frameNStart = frameN  # exact frame index
            timeout.tStart = t  # local t and not account for scr refresh
            timeout.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(timeout, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'timeout.started')
            # update status
            timeout.status = STARTED
            timeout.setAutoDraw(True)
        
        # if timeout is active this frame...
        if timeout.status == STARTED:
            # update params
            pass
        
        # *breakend* updates
        waitOnFlip = False
        
        # if breakend is starting this frame...
        if breakend.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            breakend.frameNStart = frameN  # exact frame index
            breakend.tStart = t  # local t and not account for scr refresh
            breakend.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(breakend, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'breakend.started')
            # update status
            breakend.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(breakend.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(breakend.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if breakend.status == STARTED and not waitOnFlip:
            theseKeys = breakend.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _breakend_allKeys.extend(theseKeys)
            if len(_breakend_allKeys):
                breakend.keys = _breakend_allKeys[-1].name  # just the last key pressed
                breakend.rt = _breakend_allKeys[-1].rt
                breakend.duration = _breakend_allKeys[-1].duration
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
    # check responses
    if breakend.keys in ['', [], None]:  # No response was made
        breakend.keys = None
    thisExp.addData('breakend.keys',breakend.keys)
    if breakend.keys != None:  # we had a response
        thisExp.addData('breakend.rt', breakend.rt)
        thisExp.addData('breakend.duration', breakend.duration)
    thisExp.nextEntry()
    # the Routine "rest" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    block2 = data.TrialHandler2(
        name='block2',
        nReps=1,
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('stimuli/block2.csv'), 
        seed=45, 
        isTrials=True, 
    )
    thisExp.addLoop(block2)  # add the loop to the experiment
    thisBlock2 = block2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock2.rgb)
    if thisBlock2 != None:
        for paramName in thisBlock2:
            globals()[paramName] = thisBlock2[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock2 in block2:
        block2.status = STARTED
        if hasattr(thisBlock2, 'status'):
            thisBlock2.status = STARTED
        currentLoop = block2
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock2.rgb)
        if thisBlock2 != None:
            for paramName in thisBlock2:
                globals()[paramName] = thisBlock2[paramName]
        
        # --- Prepare to start Routine "study_stage" ---
        # create an object to store info about Routine study_stage
        study_stage = data.Routine(
            name='study_stage',
            components=[Fix, stim1, stim2, audi1, audi2],
        )
        study_stage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from StudyCode
        
        
        stim1.setFillColor(color1_target)
        stim1.setOpacity(1.0)
        stim1.setPos((-200, 0))
        stim2.setFillColor(color2_target)
        stim2.setOpacity(None)
        stim2.setPos((200,0))
        audi1.setSound(audio1_target_file, secs=1, hamming=True)
        audi1.setVolume(1.0, log=False)
        audi1.seek(0)
        audi2.setSound(audio2_target_file, secs=1, hamming=True)
        audi2.setVolume(1.0, log=False)
        audi2.seek(0)
        # store start times for study_stage
        study_stage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study_stage.tStart = globalClock.getTime(format='float')
        study_stage.status = STARTED
        thisExp.addData('study_stage.started', study_stage.tStart)
        study_stage.maxDuration = None
        # keep track of which components have finished
        study_stageComponents = study_stage.components
        for thisComponent in study_stage.components:
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
        
        # --- Run Routine "study_stage" ---
        thisExp.currentRoutine = study_stage
        study_stage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.3:
            # if trial has changed, end Routine now
            if hasattr(thisBlock2, 'status') and thisBlock2.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            
            # if Fix is starting this frame...
            if Fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fix.frameNStart = frameN  # exact frame index
                Fix.tStart = t  # local t and not account for scr refresh
                Fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fix.started')
                # update status
                Fix.status = STARTED
                Fix.setAutoDraw(True)
            
            # if Fix is active this frame...
            if Fix.status == STARTED:
                # update params
                pass
            
            # if Fix is stopping this frame...
            if Fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fix.tStartRefresh + .3-frameTolerance:
                    # keep track of stop time/frame for later
                    Fix.tStop = t  # not accounting for scr refresh
                    Fix.tStopRefresh = tThisFlipGlobal  # on global time
                    Fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fix.stopped')
                    # update status
                    Fix.status = FINISHED
                    Fix.setAutoDraw(False)
            
            # *stim1* updates
            
            # if stim1 is starting this frame...
            if stim1.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                # keep track of start time/frame for later
                stim1.frameNStart = frameN  # exact frame index
                stim1.tStart = t  # local t and not account for scr refresh
                stim1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim1.started')
                # update status
                stim1.status = STARTED
                stim1.setAutoDraw(True)
            
            # if stim1 is active this frame...
            if stim1.status == STARTED:
                # update params
                pass
            
            # if stim1 is stopping this frame...
            if stim1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim1.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim1.tStop = t  # not accounting for scr refresh
                    stim1.tStopRefresh = tThisFlipGlobal  # on global time
                    stim1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim1.stopped')
                    # update status
                    stim1.status = FINISHED
                    stim1.setAutoDraw(False)
            
            # *stim2* updates
            
            # if stim2 is starting this frame...
            if stim2.status == NOT_STARTED and tThisFlip >= 1.3-frameTolerance:
                # keep track of start time/frame for later
                stim2.frameNStart = frameN  # exact frame index
                stim2.tStart = t  # local t and not account for scr refresh
                stim2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim2.started')
                # update status
                stim2.status = STARTED
                stim2.setAutoDraw(True)
            
            # if stim2 is active this frame...
            if stim2.status == STARTED:
                # update params
                pass
            
            # if stim2 is stopping this frame...
            if stim2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim2.tStop = t  # not accounting for scr refresh
                    stim2.tStopRefresh = tThisFlipGlobal  # on global time
                    stim2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim2.stopped')
                    # update status
                    stim2.status = FINISHED
                    stim2.setAutoDraw(False)
            
            # *audi1* updates
            
            # if audi1 is starting this frame...
            if audi1.status == NOT_STARTED and tThisFlip >= 2.3-frameTolerance:
                # keep track of start time/frame for later
                audi1.frameNStart = frameN  # exact frame index
                audi1.tStart = t  # local t and not account for scr refresh
                audi1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi1.started', tThisFlipGlobal)
                # update status
                audi1.status = STARTED
                audi1.play(when=win)  # sync with win flip
            
            # if audi1 is stopping this frame...
            if audi1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi1.tStartRefresh + 1-frameTolerance or audi1.isFinished:
                    # keep track of stop time/frame for later
                    audi1.tStop = t  # not accounting for scr refresh
                    audi1.tStopRefresh = tThisFlipGlobal  # on global time
                    audi1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi1.stopped')
                    # update status
                    audi1.status = FINISHED
                    audi1.stop()
            
            # *audi2* updates
            
            # if audi2 is starting this frame...
            if audi2.status == NOT_STARTED and tThisFlip >= 3.3-frameTolerance:
                # keep track of start time/frame for later
                audi2.frameNStart = frameN  # exact frame index
                audi2.tStart = t  # local t and not account for scr refresh
                audi2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi2.started', tThisFlipGlobal)
                # update status
                audi2.status = STARTED
                audi2.play(when=win)  # sync with win flip
            
            # if audi2 is stopping this frame...
            if audi2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi2.tStartRefresh + 1-frameTolerance or audi2.isFinished:
                    # keep track of stop time/frame for later
                    audi2.tStop = t  # not accounting for scr refresh
                    audi2.tStopRefresh = tThisFlipGlobal  # on global time
                    audi2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi2.stopped')
                    # update status
                    audi2.status = FINISHED
                    audi2.stop()
            
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
                    currentRoutine=study_stage,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study_stage.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study_stage.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study_stage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study_stage" ---
        for thisComponent in study_stage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study_stage
        study_stage.tStop = globalClock.getTime(format='float')
        study_stage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study_stage.stopped', study_stage.tStop)
        audi1.pause()  # ensure sound has stopped at end of Routine
        audi2.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if study_stage.maxDurationReached:
            routineTimer.addTime(-study_stage.maxDuration)
        elif study_stage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.300000)

        # Generate stratified conditions for 9 probe trials
        probe_conditions = generate_stratified_conditions()
        probe_idx = 0

        # set up handler to look after randomisation of conditions etc
        SFT_2 = data.TrialHandler2(
            name='SFT_2',
            nReps=9,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=[None],
            seed=None,
            isTrials=True,
        )
        thisExp.addLoop(SFT_2)  # add the loop to the experiment
        thisSFT_2 = SFT_2.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSFT_2.rgb)
        if thisSFT_2 != None:
            for paramName in thisSFT_2:
                globals()[paramName] = thisSFT_2[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisSFT_2 in SFT_2:
            SFT_2.status = STARTED
            if hasattr(thisSFT_2, 'status'):
                thisSFT_2.status = STARTED
            currentLoop = SFT_2
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisSFT_2.rgb)
            if thisSFT_2 != None:
                for paramName in thisSFT_2:
                    globals()[paramName] = thisSFT_2[paramName]

            # --- Prepare to start Routine "probe" ---
            # create an object to store info about Routine probe
            probe = data.Routine(
                name='probe',
                components=[Fixation, targetV, targetA, ResponseBox],
            )
            probe.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from ProbeCode
            # Use pre-generated stratified condition
            condition = probe_conditions[probe_idx]
            probe_idx += 1
            #AX AX= color, XA= audio
            #AA=0 HA =1 LA = 2
            #AH=3 HH=4 LH=5
            #AL=6 HL=7 LL=8
            if condition == 0 :#AA .25
               targetCol = color1_target
               targetAud = audio1_target_file
            elif condition == 1:#AA.25
                targetCol = color2_target
                targetAud = audio2_target_file
            if condition == 2:#HA
               targetCol = color1_target
               targetAud = audio1_H_file
            elif condition == 3:#HA
                targetCol = color2_target
                targetAud = audio2_H_file
            if condition == 4:#LA
               targetCol = color1_target
               targetAud = audio1_L_file
            elif condition == 5:#LA
                targetCol = color2_target
                targetAud = audio2_L_file
            if condition == 6:#AH
               targetCol = color1_H
               targetAud = audio1_target_file
            elif condition == 7:#AH
                targetCol = color2_H
                targetAud = audio2_target_file
            if condition == 8:#HH
               targetCol = color1_H
               targetAud = audio1_H_file
            elif condition == 9:#HH
                targetCol = color2_H
                targetAud = audio2_H_file
            if condition == 10:#LH
               targetCol = color1_L
               targetAud = audio1_H_file
            elif condition == 11:#LH
                targetCol = color2_L
                targetAud = audio2_H_file
            if condition == 12: #AL
               targetCol = color1_L
               targetAud = audio1_target_file
            elif condition == 13: #AL
                targetCol = color2_L
                targetAud = audio2_target_file
            if condition == 14:#HL
               targetCol = color1_H
               targetAud = audio1_L_file
            elif condition == 15:#HL
                targetCol = color2_H
                targetAud = audio2_L_file
            if condition == 16:#LL
               targetCol = color1_L
               targetAud = audio1_L_file
            elif condition == 17:#LL
                targetCol = color2_L
                targetAud = audio2_L_file
            
            targetV.setFillColor(targetCol)
            targetV.setPos((0,0))
            targetA.setSound(targetAud, secs=1, hamming=True)
            targetA.setVolume(1.0, log=False)
            targetA.seek(0)
            ResponseBox.keys = []  # to store response values
            ResponseBox.rt = []
            ResponseBox.status = NOT_STARTED
            # store start times for probe
            probe.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            probe.tStart = globalClock.getTime(format='float')
            probe.status = STARTED
            thisExp.addData('probe.started', probe.tStart)
            probe.maxDuration = None
            # keep track of which components have finished
            probeComponents = probe.components
            for thisComponent in probe.components:
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
            
            # --- Run Routine "probe" ---
            thisExp.currentRoutine = probe
            probe.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 3.3:
                # if trial has changed, end Routine now
                if hasattr(thisSFT_2, 'status') and thisSFT_2.status == STOPPING:
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
                    if tThisFlipGlobal > Fixation.tStartRefresh + .3-frameTolerance:
                        # keep track of stop time/frame for later
                        Fixation.tStop = t  # not accounting for scr refresh
                        Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        Fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Fixation.stopped')
                        # update status
                        Fixation.status = FINISHED
                        Fixation.setAutoDraw(False)
                
                # *targetV* updates
                
                # if targetV is starting this frame...
                if targetV.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetV.frameNStart = frameN  # exact frame index
                    targetV.tStart = t  # local t and not account for scr refresh
                    targetV.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(targetV, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetV.started')
                    # update status
                    targetV.status = STARTED
                    targetV.setAutoDraw(True)
                
                # if targetV is active this frame...
                if targetV.status == STARTED:
                    # update params
                    pass
                
                # if targetV is stopping this frame...
                if targetV.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetV.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        targetV.tStop = t  # not accounting for scr refresh
                        targetV.tStopRefresh = tThisFlipGlobal  # on global time
                        targetV.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetV.stopped')
                        # update status
                        targetV.status = FINISHED
                        targetV.setAutoDraw(False)
                
                # *targetA* updates
                
                # if targetA is starting this frame...
                if targetA.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetA.frameNStart = frameN  # exact frame index
                    targetA.tStart = t  # local t and not account for scr refresh
                    targetA.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('targetA.started', tThisFlipGlobal)
                    # update status
                    targetA.status = STARTED
                    targetA.play(when=win)  # sync with win flip
                
                # if targetA is stopping this frame...
                if targetA.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetA.tStartRefresh + 1-frameTolerance or targetA.isFinished:
                        # keep track of stop time/frame for later
                        targetA.tStop = t  # not accounting for scr refresh
                        targetA.tStopRefresh = tThisFlipGlobal  # on global time
                        targetA.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetA.stopped')
                        # update status
                        targetA.status = FINISHED
                        targetA.stop()
                # *ResponseBox* updates
                
                # if ResponseBox is starting this frame...
                if ResponseBox.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    ResponseBox.frameNStart = frameN  # exact frame index
                    ResponseBox.tStart = t  # local t and not account for scr refresh
                    ResponseBox.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ResponseBox, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    ResponseBox.status = STARTED
                    ResponseBox.clock.reset()  # now t=0
                    # clear keyboard responses
                    ResponseBox.keys = []
                    ResponseBox.rt = []
                    ResponseBox.clearEvents(eventType='keyboard')
                
                # if ResponseBox is stopping this frame...
                if ResponseBox.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ResponseBox.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        ResponseBox.tStop = t  # not accounting for scr refresh
                        ResponseBox.tStopRefresh = tThisFlipGlobal  # on global time
                        ResponseBox.frameNStop = frameN  # exact frame index
                        # update status
                        ResponseBox.status = FINISHED
                if ResponseBox.status == STARTED:
                    # check for key presses using keyboard
                    theseKeys = ResponseBox.getKeys(keyList=['y', 'n'], ignoreKeys=["escape"], waitRelease=False)
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if ResponseBox.keys == []:  # then this is first keypress
                            ResponseBox.keys = theseKeys[0].name  # 'y' or 'n'
                            ResponseBox.rt = theseKeys[0].rt
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
                        currentRoutine=probe,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    probe.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if probe.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in probe.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "probe" ---
            for thisComponent in probe.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for probe
            probe.tStop = globalClock.getTime(format='float')
            probe.tStopRefresh = tThisFlipGlobal
            thisExp.addData('probe.stopped', probe.tStop)
            # Run 'End Routine' code from ProbeCode
            # Check if the hardware was actually found and a response was made
            #if ResponseBox is not None and hasattr(ResponseBox, 'duration'):
            #    if ResponseBox.duration is not None:
            #        thisExp.addData('ResponseBox.duration', ResponseBox.duration)
            # Check if the hardware was initialized and a response occurred
            if ResponseBox is not None:
                # Use getattr to safely check for 'duration' without crashing
                resp_dur = getattr(ResponseBox, 'duration', None)
                if resp_dur is not None:
                    thisExp.addData('ResponseBox.duration', resp_dur)
                else:
                    thisExp.addData('ResponseBox.duration', 'no_response')
            else:
                thisExp.addData('ResponseBox.duration', 'device_not_found')
            thisExp.addData('condition', condition)
            thisExp.addData('TargetA', targetAud)
            thisExp.addData('TargetC', targetCol)
            
            targetA.pause()  # ensure sound has stopped at end of Routine
            # check responses
            if ResponseBox.keys in ['', [], None]:  # No response was made
                ResponseBox.keys = None
            SFT_2.addData('ResponseBox.keys',ResponseBox.keys)
            if ResponseBox.keys != None:  # we had a response
                SFT_2.addData('ResponseBox.rt', ResponseBox.rt)
            #   SFT_2.addData('ResponseBox.duration', ResponseBox.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if probe.maxDurationReached:
                routineTimer.addTime(-probe.maxDuration)
            elif probe.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-3.300000)
            # mark thisSFT_2 as finished
            if hasattr(thisSFT_2, 'status'):
                thisSFT_2.status = FINISHED
            # if awaiting a pause, pause now
            if SFT_2.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                SFT_2.status = STARTED
            thisExp.nextEntry()
            
        # completed 9 repeats of 'SFT_2'
        SFT_2.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisBlock2 as finished
        if hasattr(thisBlock2, 'status'):
            thisBlock2.status = FINISHED
        # if awaiting a pause, pause now
        if block2.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            block2.status = STARTED
        thisExp.nextEntry()
        
    # completed 25 repeats of 'block2'
    block2.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "rest" ---
    # create an object to store info about Routine rest
    rest = data.Routine(
        name='rest',
        components=[timeout, breakend],
    )
    rest.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for breakend
    breakend.keys = []
    breakend.rt = []
    _breakend_allKeys = []
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
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *timeout* updates
        
        # if timeout is starting this frame...
        if timeout.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            timeout.frameNStart = frameN  # exact frame index
            timeout.tStart = t  # local t and not account for scr refresh
            timeout.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(timeout, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'timeout.started')
            # update status
            timeout.status = STARTED
            timeout.setAutoDraw(True)
        
        # if timeout is active this frame...
        if timeout.status == STARTED:
            # update params
            pass
        
        # *breakend* updates
        waitOnFlip = False
        
        # if breakend is starting this frame...
        if breakend.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            breakend.frameNStart = frameN  # exact frame index
            breakend.tStart = t  # local t and not account for scr refresh
            breakend.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(breakend, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'breakend.started')
            # update status
            breakend.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(breakend.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(breakend.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if breakend.status == STARTED and not waitOnFlip:
            theseKeys = breakend.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _breakend_allKeys.extend(theseKeys)
            if len(_breakend_allKeys):
                breakend.keys = _breakend_allKeys[-1].name  # just the last key pressed
                breakend.rt = _breakend_allKeys[-1].rt
                breakend.duration = _breakend_allKeys[-1].duration
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
    # check responses
    if breakend.keys in ['', [], None]:  # No response was made
        breakend.keys = None
    thisExp.addData('breakend.keys',breakend.keys)
    if breakend.keys != None:  # we had a response
        thisExp.addData('breakend.rt', breakend.rt)
        thisExp.addData('breakend.duration', breakend.duration)
    thisExp.nextEntry()
    # the Routine "rest" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    block3 = data.TrialHandler2(
        name='block3',
        nReps=1,
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('stimuli/block3.csv'), 
        seed=45, 
        isTrials=True, 
    )
    thisExp.addLoop(block3)  # add the loop to the experiment
    thisBlock3 = block3.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock3.rgb)
    if thisBlock3 != None:
        for paramName in thisBlock3:
            globals()[paramName] = thisBlock3[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock3 in block3:
        block3.status = STARTED
        if hasattr(thisBlock3, 'status'):
            thisBlock3.status = STARTED
        currentLoop = block3
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock3.rgb)
        if thisBlock3 != None:
            for paramName in thisBlock3:
                globals()[paramName] = thisBlock3[paramName]
        
        # --- Prepare to start Routine "study_stage" ---
        # create an object to store info about Routine study_stage
        study_stage = data.Routine(
            name='study_stage',
            components=[Fix, stim1, stim2, audi1, audi2],
        )
        study_stage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from StudyCode
        
        
        stim1.setFillColor(color1_target)
        stim1.setOpacity(1.0)
        stim1.setPos((-200, 0))
        stim2.setFillColor(color2_target)
        stim2.setOpacity(None)
        stim2.setPos((200,0))
        audi1.setSound(audio1_target_file, secs=1, hamming=True)
        audi1.setVolume(1.0, log=False)
        audi1.seek(0)
        audi2.setSound(audio2_target_file, secs=1, hamming=True)
        audi2.setVolume(1.0, log=False)
        audi2.seek(0)
        # store start times for study_stage
        study_stage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study_stage.tStart = globalClock.getTime(format='float')
        study_stage.status = STARTED
        thisExp.addData('study_stage.started', study_stage.tStart)
        study_stage.maxDuration = None
        # keep track of which components have finished
        study_stageComponents = study_stage.components
        for thisComponent in study_stage.components:
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
        
        # --- Run Routine "study_stage" ---
        thisExp.currentRoutine = study_stage
        study_stage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.3:
            # if trial has changed, end Routine now
            if hasattr(thisBlock3, 'status') and thisBlock3.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            
            # if Fix is starting this frame...
            if Fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fix.frameNStart = frameN  # exact frame index
                Fix.tStart = t  # local t and not account for scr refresh
                Fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fix.started')
                # update status
                Fix.status = STARTED
                Fix.setAutoDraw(True)
            
            # if Fix is active this frame...
            if Fix.status == STARTED:
                # update params
                pass
            
            # if Fix is stopping this frame...
            if Fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fix.tStartRefresh + .3-frameTolerance:
                    # keep track of stop time/frame for later
                    Fix.tStop = t  # not accounting for scr refresh
                    Fix.tStopRefresh = tThisFlipGlobal  # on global time
                    Fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fix.stopped')
                    # update status
                    Fix.status = FINISHED
                    Fix.setAutoDraw(False)
            
            # *stim1* updates
            
            # if stim1 is starting this frame...
            if stim1.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                # keep track of start time/frame for later
                stim1.frameNStart = frameN  # exact frame index
                stim1.tStart = t  # local t and not account for scr refresh
                stim1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim1.started')
                # update status
                stim1.status = STARTED
                stim1.setAutoDraw(True)
            
            # if stim1 is active this frame...
            if stim1.status == STARTED:
                # update params
                pass
            
            # if stim1 is stopping this frame...
            if stim1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim1.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim1.tStop = t  # not accounting for scr refresh
                    stim1.tStopRefresh = tThisFlipGlobal  # on global time
                    stim1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim1.stopped')
                    # update status
                    stim1.status = FINISHED
                    stim1.setAutoDraw(False)
            
            # *stim2* updates
            
            # if stim2 is starting this frame...
            if stim2.status == NOT_STARTED and tThisFlip >= 1.3-frameTolerance:
                # keep track of start time/frame for later
                stim2.frameNStart = frameN  # exact frame index
                stim2.tStart = t  # local t and not account for scr refresh
                stim2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim2.started')
                # update status
                stim2.status = STARTED
                stim2.setAutoDraw(True)
            
            # if stim2 is active this frame...
            if stim2.status == STARTED:
                # update params
                pass
            
            # if stim2 is stopping this frame...
            if stim2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim2.tStop = t  # not accounting for scr refresh
                    stim2.tStopRefresh = tThisFlipGlobal  # on global time
                    stim2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim2.stopped')
                    # update status
                    stim2.status = FINISHED
                    stim2.setAutoDraw(False)
            
            # *audi1* updates
            
            # if audi1 is starting this frame...
            if audi1.status == NOT_STARTED and tThisFlip >= 2.3-frameTolerance:
                # keep track of start time/frame for later
                audi1.frameNStart = frameN  # exact frame index
                audi1.tStart = t  # local t and not account for scr refresh
                audi1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi1.started', tThisFlipGlobal)
                # update status
                audi1.status = STARTED
                audi1.play(when=win)  # sync with win flip
            
            # if audi1 is stopping this frame...
            if audi1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi1.tStartRefresh + 1-frameTolerance or audi1.isFinished:
                    # keep track of stop time/frame for later
                    audi1.tStop = t  # not accounting for scr refresh
                    audi1.tStopRefresh = tThisFlipGlobal  # on global time
                    audi1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi1.stopped')
                    # update status
                    audi1.status = FINISHED
                    audi1.stop()
            
            # *audi2* updates
            
            # if audi2 is starting this frame...
            if audi2.status == NOT_STARTED and tThisFlip >= 3.3-frameTolerance:
                # keep track of start time/frame for later
                audi2.frameNStart = frameN  # exact frame index
                audi2.tStart = t  # local t and not account for scr refresh
                audi2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi2.started', tThisFlipGlobal)
                # update status
                audi2.status = STARTED
                audi2.play(when=win)  # sync with win flip
            
            # if audi2 is stopping this frame...
            if audi2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi2.tStartRefresh + 1-frameTolerance or audi2.isFinished:
                    # keep track of stop time/frame for later
                    audi2.tStop = t  # not accounting for scr refresh
                    audi2.tStopRefresh = tThisFlipGlobal  # on global time
                    audi2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi2.stopped')
                    # update status
                    audi2.status = FINISHED
                    audi2.stop()
            
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
                    currentRoutine=study_stage,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study_stage.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study_stage.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study_stage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study_stage" ---
        for thisComponent in study_stage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study_stage
        study_stage.tStop = globalClock.getTime(format='float')
        study_stage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study_stage.stopped', study_stage.tStop)
        audi1.pause()  # ensure sound has stopped at end of Routine
        audi2.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if study_stage.maxDurationReached:
            routineTimer.addTime(-study_stage.maxDuration)
        elif study_stage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.300000)

        # Generate stratified conditions for 9 probe trials
        probe_conditions = generate_stratified_conditions()
        probe_idx = 0

        # set up handler to look after randomisation of conditions etc
        SFT_3 = data.TrialHandler2(
            name='SFT_3',
            nReps=9,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=[None],
            seed=None,
            isTrials=True,
        )
        thisExp.addLoop(SFT_3)  # add the loop to the experiment
        thisSFT_3 = SFT_3.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSFT_3.rgb)
        if thisSFT_3 != None:
            for paramName in thisSFT_3:
                globals()[paramName] = thisSFT_3[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()

        for thisSFT_3 in SFT_3:
            SFT_3.status = STARTED
            if hasattr(thisSFT_3, 'status'):
                thisSFT_3.status = STARTED
            currentLoop = SFT_3
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisSFT_3.rgb)
            if thisSFT_3 != None:
                for paramName in thisSFT_3:
                    globals()[paramName] = thisSFT_3[paramName]

            # --- Prepare to start Routine "probe" ---
            # create an object to store info about Routine probe
            probe = data.Routine(
                name='probe',
                components=[Fixation, targetV, targetA, ResponseBox],
            )
            probe.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from ProbeCode
            # Use pre-generated stratified condition
            condition = probe_conditions[probe_idx]
            probe_idx += 1
            # Old random code removed - now using stratified conditions
            #AX AX= color, XA= audio
            #AA=0 HA =1 LA = 2
            #AH=3 HH=4 LH=5
            #AL=6 HL=7 LL=8
            if condition == 0 :#AA .25
               targetCol = color1_target
               targetAud = audio1_target_file
            elif condition == 1:#AA.25
                targetCol = color2_target
                targetAud = audio2_target_file
            if condition == 2:#HA
               targetCol = color1_target
               targetAud = audio1_H_file
            elif condition == 3:#HA
                targetCol = color2_target
                targetAud = audio2_H_file
            if condition == 4:#LA
               targetCol = color1_target
               targetAud = audio1_L_file
            elif condition == 5:#LA
                targetCol = color2_target
                targetAud = audio2_L_file
            if condition == 6:#AH
               targetCol = color1_H
               targetAud = audio1_target_file
            elif condition == 7:#AH
                targetCol = color2_H
                targetAud = audio2_target_file
            if condition == 8:#HH
               targetCol = color1_H
               targetAud = audio1_H_file
            elif condition == 9:#HH
                targetCol = color2_H
                targetAud = audio2_H_file
            if condition == 10:#LH
               targetCol = color1_L
               targetAud = audio1_H_file
            elif condition == 11:#LH
                targetCol = color2_L
                targetAud = audio2_H_file
            if condition == 12: #AL
               targetCol = color1_L
               targetAud = audio1_target_file
            elif condition == 13: #AL
                targetCol = color2_L
                targetAud = audio2_target_file
            if condition == 14:#HL
               targetCol = color1_H
               targetAud = audio1_L_file
            elif condition == 15:#HL
                targetCol = color2_H
                targetAud = audio2_L_file
            if condition == 16:#LL
               targetCol = color1_L
               targetAud = audio1_L_file
            elif condition == 17:#LL
                targetCol = color2_L
                targetAud = audio2_L_file
            
            targetV.setFillColor(targetCol)
            targetV.setPos((0,0))
            targetA.setSound(targetAud, secs=1, hamming=True)
            targetA.setVolume(1.0, log=False)
            targetA.seek(0)
            ResponseBox.keys = []  # to store response values
            ResponseBox.rt = []
            ResponseBox.status = NOT_STARTED
            # store start times for probe
            probe.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            probe.tStart = globalClock.getTime(format='float')
            probe.status = STARTED
            thisExp.addData('probe.started', probe.tStart)
            probe.maxDuration = None
            # keep track of which components have finished
            probeComponents = probe.components
            for thisComponent in probe.components:
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
            
            # --- Run Routine "probe" ---
            thisExp.currentRoutine = probe
            probe.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 3.3:
                # if trial has changed, end Routine now
                if hasattr(thisSFT_3, 'status') and thisSFT_3.status == STOPPING:
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
                    if tThisFlipGlobal > Fixation.tStartRefresh + .3-frameTolerance:
                        # keep track of stop time/frame for later
                        Fixation.tStop = t  # not accounting for scr refresh
                        Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        Fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Fixation.stopped')
                        # update status
                        Fixation.status = FINISHED
                        Fixation.setAutoDraw(False)
                
                # *targetV* updates
                
                # if targetV is starting this frame...
                if targetV.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetV.frameNStart = frameN  # exact frame index
                    targetV.tStart = t  # local t and not account for scr refresh
                    targetV.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(targetV, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetV.started')
                    # update status
                    targetV.status = STARTED
                    targetV.setAutoDraw(True)
                
                # if targetV is active this frame...
                if targetV.status == STARTED:
                    # update params
                    pass
                
                # if targetV is stopping this frame...
                if targetV.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetV.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        targetV.tStop = t  # not accounting for scr refresh
                        targetV.tStopRefresh = tThisFlipGlobal  # on global time
                        targetV.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetV.stopped')
                        # update status
                        targetV.status = FINISHED
                        targetV.setAutoDraw(False)
                
                # *targetA* updates
                
                # if targetA is starting this frame...
                if targetA.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetA.frameNStart = frameN  # exact frame index
                    targetA.tStart = t  # local t and not account for scr refresh
                    targetA.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('targetA.started', tThisFlipGlobal)
                    # update status
                    targetA.status = STARTED
                    targetA.play(when=win)  # sync with win flip
                
                # if targetA is stopping this frame...
                if targetA.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetA.tStartRefresh + 1-frameTolerance or targetA.isFinished:
                        # keep track of stop time/frame for later
                        targetA.tStop = t  # not accounting for scr refresh
                        targetA.tStopRefresh = tThisFlipGlobal  # on global time
                        targetA.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetA.stopped')
                        # update status
                        targetA.status = FINISHED
                        targetA.stop()
                # *ResponseBox* updates
                
                # if ResponseBox is starting this frame...
                if ResponseBox.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    ResponseBox.frameNStart = frameN  # exact frame index
                    ResponseBox.tStart = t  # local t and not account for scr refresh
                    ResponseBox.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ResponseBox, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    ResponseBox.status = STARTED
                    ResponseBox.clock.reset()  # now t=0
                    # clear keyboard responses
                    ResponseBox.keys = []
                    ResponseBox.rt = []
                    ResponseBox.clearEvents(eventType='keyboard')
                
                # if ResponseBox is stopping this frame...
                if ResponseBox.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ResponseBox.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        ResponseBox.tStop = t  # not accounting for scr refresh
                        ResponseBox.tStopRefresh = tThisFlipGlobal  # on global time
                        ResponseBox.frameNStop = frameN  # exact frame index
                        # update status
                        ResponseBox.status = FINISHED
                if ResponseBox.status == STARTED:
                    # check for key presses using keyboard
                    theseKeys = ResponseBox.getKeys(keyList=['y', 'n'], ignoreKeys=["escape"], waitRelease=False)
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if ResponseBox.keys == []:  # then this is first keypress
                            ResponseBox.keys = theseKeys[0].name  # 'y' or 'n'
                            ResponseBox.rt = theseKeys[0].rt
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
                        currentRoutine=probe,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    probe.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if probe.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in probe.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "probe" ---
            for thisComponent in probe.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for probe
            probe.tStop = globalClock.getTime(format='float')
            probe.tStopRefresh = tThisFlipGlobal
            thisExp.addData('probe.stopped', probe.tStop)
            # Run 'End Routine' code from ProbeCode
            # Check if the hardware was actually found and a response was made
            #if ResponseBox is not None and hasattr(ResponseBox, 'duration'):
            #    if ResponseBox.duration is not None:
            #        thisExp.addData('ResponseBox.duration', ResponseBox.duration)
            # Check if the hardware was initialized and a response occurred
            if ResponseBox is not None:
                # Use getattr to safely check for 'duration' without crashing
                resp_dur = getattr(ResponseBox, 'duration', None)
                if resp_dur is not None:
                    thisExp.addData('ResponseBox.duration', resp_dur)
                else:
                    thisExp.addData('ResponseBox.duration', 'no_response')
            else:
                thisExp.addData('ResponseBox.duration', 'device_not_found')
            thisExp.addData('condition', condition)
            thisExp.addData('TargetA', targetAud)
            thisExp.addData('TargetC', targetCol)
            
            targetA.pause()  # ensure sound has stopped at end of Routine
            # check responses
            if ResponseBox.keys in ['', [], None]:  # No response was made
                ResponseBox.keys = None
            SFT_3.addData('ResponseBox.keys',ResponseBox.keys)
            if ResponseBox.keys != None:  # we had a response
                SFT_3.addData('ResponseBox.rt', ResponseBox.rt)
            #    SFT_3.addData('ResponseBox.duration', ResponseBox.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if probe.maxDurationReached:
                routineTimer.addTime(-probe.maxDuration)
            elif probe.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-3.300000)
            # mark thisSFT_3 as finished
            if hasattr(thisSFT_3, 'status'):
                thisSFT_3.status = FINISHED
            # if awaiting a pause, pause now
            if SFT_3.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                SFT_3.status = STARTED
            thisExp.nextEntry()
            
        # completed 9 repeats of 'SFT_3'
        SFT_3.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisBlock3 as finished
        if hasattr(thisBlock3, 'status'):
            thisBlock3.status = FINISHED
        # if awaiting a pause, pause now
        if block3.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            block3.status = STARTED
        thisExp.nextEntry()
        
    # completed 25 repeats of 'block3'
    block3.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # set up handler to look after randomisation of conditions etc
    block4 = data.TrialHandler2(
        name='block4',
        nReps=1,
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=45, 
        isTrials=True, 
    )
    thisExp.addLoop(block4)  # add the loop to the experiment
    thisBlock4 = block4.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock4.rgb)
    if thisBlock4 != None:
        for paramName in thisBlock4:
            globals()[paramName] = thisBlock4[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock4 in block4:
        block4.status = STARTED
        if hasattr(thisBlock4, 'status'):
            thisBlock4.status = STARTED
        currentLoop = block4
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock4.rgb)
        if thisBlock4 != None:
            for paramName in thisBlock4:
                globals()[paramName] = thisBlock4[paramName]
        
        # --- Prepare to start Routine "study_stage" ---
        # create an object to store info about Routine study_stage
        study_stage = data.Routine(
            name='study_stage',
            components=[Fix, stim1, stim2, audi1, audi2],
        )
        study_stage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from StudyCode
        
        
        stim1.setFillColor(color1_target)
        stim1.setOpacity(1.0)
        stim1.setPos((-200, 0))
        stim2.setFillColor(color2_target)
        stim2.setOpacity(None)
        stim2.setPos((200,0))
        audi1.setSound(audio1_target_file, secs=1, hamming=True)
        audi1.setVolume(1.0, log=False)
        audi1.seek(0)
        audi2.setSound(audio2_target_file, secs=1, hamming=True)
        audi2.setVolume(1.0, log=False)
        audi2.seek(0)
        # store start times for study_stage
        study_stage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study_stage.tStart = globalClock.getTime(format='float')
        study_stage.status = STARTED
        thisExp.addData('study_stage.started', study_stage.tStart)
        study_stage.maxDuration = None
        # keep track of which components have finished
        study_stageComponents = study_stage.components
        for thisComponent in study_stage.components:
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
        
        # --- Run Routine "study_stage" ---
        thisExp.currentRoutine = study_stage
        study_stage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.3:
            # if trial has changed, end Routine now
            if hasattr(thisBlock4, 'status') and thisBlock4.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            
            # if Fix is starting this frame...
            if Fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fix.frameNStart = frameN  # exact frame index
                Fix.tStart = t  # local t and not account for scr refresh
                Fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fix.started')
                # update status
                Fix.status = STARTED
                Fix.setAutoDraw(True)
            
            # if Fix is active this frame...
            if Fix.status == STARTED:
                # update params
                pass
            
            # if Fix is stopping this frame...
            if Fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fix.tStartRefresh + .3-frameTolerance:
                    # keep track of stop time/frame for later
                    Fix.tStop = t  # not accounting for scr refresh
                    Fix.tStopRefresh = tThisFlipGlobal  # on global time
                    Fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fix.stopped')
                    # update status
                    Fix.status = FINISHED
                    Fix.setAutoDraw(False)
            
            # *stim1* updates
            
            # if stim1 is starting this frame...
            if stim1.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                # keep track of start time/frame for later
                stim1.frameNStart = frameN  # exact frame index
                stim1.tStart = t  # local t and not account for scr refresh
                stim1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim1.started')
                # update status
                stim1.status = STARTED
                stim1.setAutoDraw(True)
            
            # if stim1 is active this frame...
            if stim1.status == STARTED:
                # update params
                pass
            
            # if stim1 is stopping this frame...
            if stim1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim1.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim1.tStop = t  # not accounting for scr refresh
                    stim1.tStopRefresh = tThisFlipGlobal  # on global time
                    stim1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim1.stopped')
                    # update status
                    stim1.status = FINISHED
                    stim1.setAutoDraw(False)
            
            # *stim2* updates
            
            # if stim2 is starting this frame...
            if stim2.status == NOT_STARTED and tThisFlip >= 1.3-frameTolerance:
                # keep track of start time/frame for later
                stim2.frameNStart = frameN  # exact frame index
                stim2.tStart = t  # local t and not account for scr refresh
                stim2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim2.started')
                # update status
                stim2.status = STARTED
                stim2.setAutoDraw(True)
            
            # if stim2 is active this frame...
            if stim2.status == STARTED:
                # update params
                pass
            
            # if stim2 is stopping this frame...
            if stim2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim2.tStop = t  # not accounting for scr refresh
                    stim2.tStopRefresh = tThisFlipGlobal  # on global time
                    stim2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim2.stopped')
                    # update status
                    stim2.status = FINISHED
                    stim2.setAutoDraw(False)
            
            # *audi1* updates
            
            # if audi1 is starting this frame...
            if audi1.status == NOT_STARTED and tThisFlip >= 2.3-frameTolerance:
                # keep track of start time/frame for later
                audi1.frameNStart = frameN  # exact frame index
                audi1.tStart = t  # local t and not account for scr refresh
                audi1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi1.started', tThisFlipGlobal)
                # update status
                audi1.status = STARTED
                audi1.play(when=win)  # sync with win flip
            
            # if audi1 is stopping this frame...
            if audi1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi1.tStartRefresh + 1-frameTolerance or audi1.isFinished:
                    # keep track of stop time/frame for later
                    audi1.tStop = t  # not accounting for scr refresh
                    audi1.tStopRefresh = tThisFlipGlobal  # on global time
                    audi1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi1.stopped')
                    # update status
                    audi1.status = FINISHED
                    audi1.stop()
            
            # *audi2* updates
            
            # if audi2 is starting this frame...
            if audi2.status == NOT_STARTED and tThisFlip >= 3.3-frameTolerance:
                # keep track of start time/frame for later
                audi2.frameNStart = frameN  # exact frame index
                audi2.tStart = t  # local t and not account for scr refresh
                audi2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi2.started', tThisFlipGlobal)
                # update status
                audi2.status = STARTED
                audi2.play(when=win)  # sync with win flip
            
            # if audi2 is stopping this frame...
            if audi2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi2.tStartRefresh + 1-frameTolerance or audi2.isFinished:
                    # keep track of stop time/frame for later
                    audi2.tStop = t  # not accounting for scr refresh
                    audi2.tStopRefresh = tThisFlipGlobal  # on global time
                    audi2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi2.stopped')
                    # update status
                    audi2.status = FINISHED
                    audi2.stop()
            
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
                    currentRoutine=study_stage,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study_stage.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study_stage.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study_stage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study_stage" ---
        for thisComponent in study_stage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study_stage
        study_stage.tStop = globalClock.getTime(format='float')
        study_stage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study_stage.stopped', study_stage.tStop)
        audi1.pause()  # ensure sound has stopped at end of Routine
        audi2.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if study_stage.maxDurationReached:
            routineTimer.addTime(-study_stage.maxDuration)
        elif study_stage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.300000)
        
        # set up handler to look after randomisation of conditions etc
        SFT_4 = data.TrialHandler2(
            name='SFT_4',
            nReps=9,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=[None],
            seed=None,
            isTrials=True,
        )
        # Generate stratified conditions for this block
        probe_conditions = generate_stratified_conditions()
        probe_idx = 0
        thisExp.addLoop(SFT_4)  # add the loop to the experiment
        thisSFT_4 = SFT_4.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSFT_4.rgb)
        if thisSFT_4 != None:
            for paramName in thisSFT_4:
                globals()[paramName] = thisSFT_4[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisSFT_4 in SFT_4:
            SFT_4.status = STARTED
            if hasattr(thisSFT_4, 'status'):
                thisSFT_4.status = STARTED
            currentLoop = SFT_4
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisSFT_4.rgb)
            if thisSFT_4 != None:
                for paramName in thisSFT_4:
                    globals()[paramName] = thisSFT_4[paramName]

            # --- Prepare to start Routine "probe" ---
            # create an object to store info about Routine probe
            probe = data.Routine(
                name='probe',
                components=[Fixation, targetV, targetA, ResponseBox],
            )
            probe.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from ProbeCode
            # Use pre-generated stratified condition
            condition = probe_conditions[probe_idx]
            probe_idx += 1
            # Old random code removed - now using stratified conditions
            #AX AX= color, XA= audio
            #AA=0 HA =1 LA = 2
            #AH=3 HH=4 LH=5
            #AL=6 HL=7 LL=8
            if condition == 0 :#AA .25
               targetCol = color1_target
               targetAud = audio1_target_file
            elif condition == 1:#AA.25
                targetCol = color2_target
                targetAud = audio2_target_file
            if condition == 2:#HA
               targetCol = color1_target
               targetAud = audio1_H_file
            elif condition == 3:#HA
                targetCol = color2_target
                targetAud = audio2_H_file
            if condition == 4:#LA
               targetCol = color1_target
               targetAud = audio1_L_file
            elif condition == 5:#LA
                targetCol = color2_target
                targetAud = audio2_L_file
            if condition == 6:#AH
               targetCol = color1_H
               targetAud = audio1_target_file
            elif condition == 7:#AH
                targetCol = color2_H
                targetAud = audio2_target_file
            if condition == 8:#HH
               targetCol = color1_H
               targetAud = audio1_H_file
            elif condition == 9:#HH
                targetCol = color2_H
                targetAud = audio2_H_file
            if condition == 10:#LH
               targetCol = color1_L
               targetAud = audio1_H_file
            elif condition == 11:#LH
                targetCol = color2_L
                targetAud = audio2_H_file
            if condition == 12: #AL
               targetCol = color1_L
               targetAud = audio1_target_file
            elif condition == 13: #AL
                targetCol = color2_L
                targetAud = audio2_target_file
            if condition == 14:#HL
               targetCol = color1_H
               targetAud = audio1_L_file
            elif condition == 15:#HL
                targetCol = color2_H
                targetAud = audio2_L_file
            if condition == 16:#LL
               targetCol = color1_L
               targetAud = audio1_L_file
            elif condition == 17:#LL
                targetCol = color2_L
                targetAud = audio2_L_file
            
            targetV.setFillColor(targetCol)
            targetV.setPos((0,0))
            targetA.setSound(targetAud, secs=1, hamming=True)
            targetA.setVolume(1.0, log=False)
            targetA.seek(0)
            ResponseBox.keys = []  # to store response values
            ResponseBox.rt = []
            ResponseBox.status = NOT_STARTED
            # store start times for probe
            probe.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            probe.tStart = globalClock.getTime(format='float')
            probe.status = STARTED
            thisExp.addData('probe.started', probe.tStart)
            probe.maxDuration = None
            # keep track of which components have finished
            probeComponents = probe.components
            for thisComponent in probe.components:
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
            
            # --- Run Routine "probe" ---
            thisExp.currentRoutine = probe
            probe.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 3.3:
                # if trial has changed, end Routine now
                if hasattr(thisSFT_4, 'status') and thisSFT_4.status == STOPPING:
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
                    if tThisFlipGlobal > Fixation.tStartRefresh + .3-frameTolerance:
                        # keep track of stop time/frame for later
                        Fixation.tStop = t  # not accounting for scr refresh
                        Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        Fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Fixation.stopped')
                        # update status
                        Fixation.status = FINISHED
                        Fixation.setAutoDraw(False)
                
                # *targetV* updates
                
                # if targetV is starting this frame...
                if targetV.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetV.frameNStart = frameN  # exact frame index
                    targetV.tStart = t  # local t and not account for scr refresh
                    targetV.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(targetV, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetV.started')
                    # update status
                    targetV.status = STARTED
                    targetV.setAutoDraw(True)
                
                # if targetV is active this frame...
                if targetV.status == STARTED:
                    # update params
                    pass
                
                # if targetV is stopping this frame...
                if targetV.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetV.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        targetV.tStop = t  # not accounting for scr refresh
                        targetV.tStopRefresh = tThisFlipGlobal  # on global time
                        targetV.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetV.stopped')
                        # update status
                        targetV.status = FINISHED
                        targetV.setAutoDraw(False)
                
                # *targetA* updates
                
                # if targetA is starting this frame...
                if targetA.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetA.frameNStart = frameN  # exact frame index
                    targetA.tStart = t  # local t and not account for scr refresh
                    targetA.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('targetA.started', tThisFlipGlobal)
                    # update status
                    targetA.status = STARTED
                    targetA.play(when=win)  # sync with win flip
                
                # if targetA is stopping this frame...
                if targetA.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetA.tStartRefresh + 1-frameTolerance or targetA.isFinished:
                        # keep track of stop time/frame for later
                        targetA.tStop = t  # not accounting for scr refresh
                        targetA.tStopRefresh = tThisFlipGlobal  # on global time
                        targetA.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetA.stopped')
                        # update status
                        targetA.status = FINISHED
                        targetA.stop()
                # *ResponseBox* updates
                
                # if ResponseBox is starting this frame...
                if ResponseBox.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    ResponseBox.frameNStart = frameN  # exact frame index
                    ResponseBox.tStart = t  # local t and not account for scr refresh
                    ResponseBox.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ResponseBox, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    ResponseBox.status = STARTED
                    ResponseBox.clock.reset()  # now t=0
                    # clear keyboard responses
                    ResponseBox.keys = []
                    ResponseBox.rt = []
                    ResponseBox.clearEvents(eventType='keyboard')
                
                # if ResponseBox is stopping this frame...
                if ResponseBox.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ResponseBox.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        ResponseBox.tStop = t  # not accounting for scr refresh
                        ResponseBox.tStopRefresh = tThisFlipGlobal  # on global time
                        ResponseBox.frameNStop = frameN  # exact frame index
                        # update status
                        ResponseBox.status = FINISHED
                if ResponseBox.status == STARTED:
                    # check for key presses using keyboard
                    theseKeys = ResponseBox.getKeys(keyList=['y', 'n'], ignoreKeys=["escape"], waitRelease=False)
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if ResponseBox.keys == []:  # then this is first keypress
                            ResponseBox.keys = theseKeys[0].name  # 'y' or 'n'
                            ResponseBox.rt = theseKeys[0].rt
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
                        currentRoutine=probe,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    probe.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if probe.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in probe.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "probe" ---
            for thisComponent in probe.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for probe
            probe.tStop = globalClock.getTime(format='float')
            probe.tStopRefresh = tThisFlipGlobal
            thisExp.addData('probe.stopped', probe.tStop)
            # Run 'End Routine' code from ProbeCode
            # Check if the hardware was actually found and a response was made
            #if ResponseBox is not None and hasattr(ResponseBox, 'duration'):
            #    if ResponseBox.duration is not None:
            #        thisExp.addData('ResponseBox.duration', ResponseBox.duration)
            # Check if the hardware was initialized and a response occurred
            if ResponseBox is not None:
                # Use getattr to safely check for 'duration' without crashing
                resp_dur = getattr(ResponseBox, 'duration', None)
                if resp_dur is not None:
                    thisExp.addData('ResponseBox.duration', resp_dur)
                else:
                    thisExp.addData('ResponseBox.duration', 'no_response')
            else:
                thisExp.addData('ResponseBox.duration', 'device_not_found')
            thisExp.addData('condition', condition)
            thisExp.addData('TargetA', targetAud)
            thisExp.addData('TargetC', targetCol)
            
            targetA.pause()  # ensure sound has stopped at end of Routine
            # check responses
            if ResponseBox.keys in ['', [], None]:  # No response was made
                ResponseBox.keys = None
            SFT_4.addData('ResponseBox.keys',ResponseBox.keys)
            if ResponseBox.keys != None:  # we had a response
                SFT_4.addData('ResponseBox.rt', ResponseBox.rt)
            #    SFT_4.addData('ResponseBox.duration', ResponseBox.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if probe.maxDurationReached:
                routineTimer.addTime(-probe.maxDuration)
            elif probe.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-3.300000)
            # mark thisSFT_4 as finished
            if hasattr(thisSFT_4, 'status'):
                thisSFT_4.status = FINISHED
            # if awaiting a pause, pause now
            if SFT_4.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                SFT_4.status = STARTED
            thisExp.nextEntry()
            
        # completed 9 repeats of 'SFT_4'
        SFT_4.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisBlock4 as finished
        if hasattr(thisBlock4, 'status'):
            thisBlock4.status = FINISHED
        # if awaiting a pause, pause now
        if block4.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            block4.status = STARTED
        thisExp.nextEntry()
        
    # completed 25 repeats of 'block4'
    block4.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "rest" ---
    # create an object to store info about Routine rest
    rest = data.Routine(
        name='rest',
        components=[timeout, breakend],
    )
    rest.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for breakend
    breakend.keys = []
    breakend.rt = []
    _breakend_allKeys = []
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
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *timeout* updates
        
        # if timeout is starting this frame...
        if timeout.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            timeout.frameNStart = frameN  # exact frame index
            timeout.tStart = t  # local t and not account for scr refresh
            timeout.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(timeout, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'timeout.started')
            # update status
            timeout.status = STARTED
            timeout.setAutoDraw(True)
        
        # if timeout is active this frame...
        if timeout.status == STARTED:
            # update params
            pass
        
        # *breakend* updates
        waitOnFlip = False
        
        # if breakend is starting this frame...
        if breakend.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            breakend.frameNStart = frameN  # exact frame index
            breakend.tStart = t  # local t and not account for scr refresh
            breakend.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(breakend, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'breakend.started')
            # update status
            breakend.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(breakend.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(breakend.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if breakend.status == STARTED and not waitOnFlip:
            theseKeys = breakend.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _breakend_allKeys.extend(theseKeys)
            if len(_breakend_allKeys):
                breakend.keys = _breakend_allKeys[-1].name  # just the last key pressed
                breakend.rt = _breakend_allKeys[-1].rt
                breakend.duration = _breakend_allKeys[-1].duration
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
    # check responses
    if breakend.keys in ['', [], None]:  # No response was made
        breakend.keys = None
    thisExp.addData('breakend.keys',breakend.keys)
    if breakend.keys != None:  # we had a response
        thisExp.addData('breakend.rt', breakend.rt)
        thisExp.addData('breakend.duration', breakend.duration)
    thisExp.nextEntry()
    # the Routine "rest" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    block5 = data.TrialHandler2(
        name='block5',
        nReps=1,
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=45, 
        isTrials=True, 
    )
    thisExp.addLoop(block5)  # add the loop to the experiment
    thisBlock5 = block5.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock5.rgb)
    if thisBlock5 != None:
        for paramName in thisBlock5:
            globals()[paramName] = thisBlock5[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock5 in block5:
        block5.status = STARTED
        if hasattr(thisBlock5, 'status'):
            thisBlock5.status = STARTED
        currentLoop = block5
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock5.rgb)
        if thisBlock5 != None:
            for paramName in thisBlock5:
                globals()[paramName] = thisBlock5[paramName]
        
        # --- Prepare to start Routine "study_stage" ---
        # create an object to store info about Routine study_stage
        study_stage = data.Routine(
            name='study_stage',
            components=[Fix, stim1, stim2, audi1, audi2],
        )
        study_stage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from StudyCode
        
        
        stim1.setFillColor(color1_target)
        stim1.setOpacity(1.0)
        stim1.setPos((-200, 0))
        stim2.setFillColor(color2_target)
        stim2.setOpacity(None)
        stim2.setPos((200,0))
        audi1.setSound(audio1_target_file, secs=1, hamming=True)
        audi1.setVolume(1.0, log=False)
        audi1.seek(0)
        audi2.setSound(audio2_target_file, secs=1, hamming=True)
        audi2.setVolume(1.0, log=False)
        audi2.seek(0)
        # store start times for study_stage
        study_stage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study_stage.tStart = globalClock.getTime(format='float')
        study_stage.status = STARTED
        thisExp.addData('study_stage.started', study_stage.tStart)
        study_stage.maxDuration = None
        # keep track of which components have finished
        study_stageComponents = study_stage.components
        for thisComponent in study_stage.components:
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
        
        # --- Run Routine "study_stage" ---
        thisExp.currentRoutine = study_stage
        study_stage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.3:
            # if trial has changed, end Routine now
            if hasattr(thisBlock5, 'status') and thisBlock5.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            
            # if Fix is starting this frame...
            if Fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fix.frameNStart = frameN  # exact frame index
                Fix.tStart = t  # local t and not account for scr refresh
                Fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fix.started')
                # update status
                Fix.status = STARTED
                Fix.setAutoDraw(True)
            
            # if Fix is active this frame...
            if Fix.status == STARTED:
                # update params
                pass
            
            # if Fix is stopping this frame...
            if Fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fix.tStartRefresh + .3-frameTolerance:
                    # keep track of stop time/frame for later
                    Fix.tStop = t  # not accounting for scr refresh
                    Fix.tStopRefresh = tThisFlipGlobal  # on global time
                    Fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fix.stopped')
                    # update status
                    Fix.status = FINISHED
                    Fix.setAutoDraw(False)
            
            # *stim1* updates
            
            # if stim1 is starting this frame...
            if stim1.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                # keep track of start time/frame for later
                stim1.frameNStart = frameN  # exact frame index
                stim1.tStart = t  # local t and not account for scr refresh
                stim1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim1.started')
                # update status
                stim1.status = STARTED
                stim1.setAutoDraw(True)
            
            # if stim1 is active this frame...
            if stim1.status == STARTED:
                # update params
                pass
            
            # if stim1 is stopping this frame...
            if stim1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim1.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim1.tStop = t  # not accounting for scr refresh
                    stim1.tStopRefresh = tThisFlipGlobal  # on global time
                    stim1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim1.stopped')
                    # update status
                    stim1.status = FINISHED
                    stim1.setAutoDraw(False)
            
            # *stim2* updates
            
            # if stim2 is starting this frame...
            if stim2.status == NOT_STARTED and tThisFlip >= 1.3-frameTolerance:
                # keep track of start time/frame for later
                stim2.frameNStart = frameN  # exact frame index
                stim2.tStart = t  # local t and not account for scr refresh
                stim2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim2.started')
                # update status
                stim2.status = STARTED
                stim2.setAutoDraw(True)
            
            # if stim2 is active this frame...
            if stim2.status == STARTED:
                # update params
                pass
            
            # if stim2 is stopping this frame...
            if stim2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim2.tStop = t  # not accounting for scr refresh
                    stim2.tStopRefresh = tThisFlipGlobal  # on global time
                    stim2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim2.stopped')
                    # update status
                    stim2.status = FINISHED
                    stim2.setAutoDraw(False)
            
            # *audi1* updates
            
            # if audi1 is starting this frame...
            if audi1.status == NOT_STARTED and tThisFlip >= 2.3-frameTolerance:
                # keep track of start time/frame for later
                audi1.frameNStart = frameN  # exact frame index
                audi1.tStart = t  # local t and not account for scr refresh
                audi1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi1.started', tThisFlipGlobal)
                # update status
                audi1.status = STARTED
                audi1.play(when=win)  # sync with win flip
            
            # if audi1 is stopping this frame...
            if audi1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi1.tStartRefresh + 1-frameTolerance or audi1.isFinished:
                    # keep track of stop time/frame for later
                    audi1.tStop = t  # not accounting for scr refresh
                    audi1.tStopRefresh = tThisFlipGlobal  # on global time
                    audi1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi1.stopped')
                    # update status
                    audi1.status = FINISHED
                    audi1.stop()
            
            # *audi2* updates
            
            # if audi2 is starting this frame...
            if audi2.status == NOT_STARTED and tThisFlip >= 3.3-frameTolerance:
                # keep track of start time/frame for later
                audi2.frameNStart = frameN  # exact frame index
                audi2.tStart = t  # local t and not account for scr refresh
                audi2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi2.started', tThisFlipGlobal)
                # update status
                audi2.status = STARTED
                audi2.play(when=win)  # sync with win flip
            
            # if audi2 is stopping this frame...
            if audi2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi2.tStartRefresh + 1-frameTolerance or audi2.isFinished:
                    # keep track of stop time/frame for later
                    audi2.tStop = t  # not accounting for scr refresh
                    audi2.tStopRefresh = tThisFlipGlobal  # on global time
                    audi2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi2.stopped')
                    # update status
                    audi2.status = FINISHED
                    audi2.stop()
            
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
                    currentRoutine=study_stage,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study_stage.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study_stage.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study_stage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study_stage" ---
        for thisComponent in study_stage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study_stage
        study_stage.tStop = globalClock.getTime(format='float')
        study_stage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study_stage.stopped', study_stage.tStop)
        audi1.pause()  # ensure sound has stopped at end of Routine
        audi2.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if study_stage.maxDurationReached:
            routineTimer.addTime(-study_stage.maxDuration)
        elif study_stage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.300000)
        
        # set up handler to look after randomisation of conditions etc
        SFT_5 = data.TrialHandler2(
            name='SFT_5',
            nReps=9,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=[None],
            seed=None,
            isTrials=True,
        )
        # Generate stratified conditions for this block
        probe_conditions = generate_stratified_conditions()
        probe_idx = 0
        thisExp.addLoop(SFT_5)  # add the loop to the experiment
        thisSFT_5 = SFT_5.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSFT_5.rgb)
        if thisSFT_5 != None:
            for paramName in thisSFT_5:
                globals()[paramName] = thisSFT_5[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisSFT_5 in SFT_5:
            SFT_5.status = STARTED
            if hasattr(thisSFT_5, 'status'):
                thisSFT_5.status = STARTED
            currentLoop = SFT_5
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisSFT_5.rgb)
            if thisSFT_5 != None:
                for paramName in thisSFT_5:
                    globals()[paramName] = thisSFT_5[paramName]

            # --- Prepare to start Routine "probe" ---
            # create an object to store info about Routine probe
            probe = data.Routine(
                name='probe',
                components=[Fixation, targetV, targetA, ResponseBox],
            )
            probe.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from ProbeCode
            # Use pre-generated stratified condition
            condition = probe_conditions[probe_idx]
            probe_idx += 1
            # Old random code removed - now using stratified conditions
            #AX AX= color, XA= audio
            #AA=0 HA =1 LA = 2
            #AH=3 HH=4 LH=5
            #AL=6 HL=7 LL=8
            if condition == 0 :#AA .25
               targetCol = color1_target
               targetAud = audio1_target_file
            elif condition == 1:#AA.25
                targetCol = color2_target
                targetAud = audio2_target_file
            if condition == 2:#HA
               targetCol = color1_target
               targetAud = audio1_H_file
            elif condition == 3:#HA
                targetCol = color2_target
                targetAud = audio2_H_file
            if condition == 4:#LA
               targetCol = color1_target
               targetAud = audio1_L_file
            elif condition == 5:#LA
                targetCol = color2_target
                targetAud = audio2_L_file
            if condition == 6:#AH
               targetCol = color1_H
               targetAud = audio1_target_file
            elif condition == 7:#AH
                targetCol = color2_H
                targetAud = audio2_target_file
            if condition == 8:#HH
               targetCol = color1_H
               targetAud = audio1_H_file
            elif condition == 9:#HH
                targetCol = color2_H
                targetAud = audio2_H_file
            if condition == 10:#LH
               targetCol = color1_L
               targetAud = audio1_H_file
            elif condition == 11:#LH
                targetCol = color2_L
                targetAud = audio2_H_file
            if condition == 12: #AL
               targetCol = color1_L
               targetAud = audio1_target_file
            elif condition == 13: #AL
                targetCol = color2_L
                targetAud = audio2_target_file
            if condition == 14:#HL
               targetCol = color1_H
               targetAud = audio1_L_file
            elif condition == 15:#HL
                targetCol = color2_H
                targetAud = audio2_L_file
            if condition == 16:#LL
               targetCol = color1_L
               targetAud = audio1_L_file
            elif condition == 17:#LL
                targetCol = color2_L
                targetAud = audio2_L_file
            
            targetV.setFillColor(targetCol)
            targetV.setPos((0,0))
            targetA.setSound(targetAud, secs=1, hamming=True)
            targetA.setVolume(1.0, log=False)
            targetA.seek(0)
            ResponseBox.keys = []  # to store response values
            ResponseBox.rt = []
            ResponseBox.status = NOT_STARTED
            # store start times for probe
            probe.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            probe.tStart = globalClock.getTime(format='float')
            probe.status = STARTED
            thisExp.addData('probe.started', probe.tStart)
            probe.maxDuration = None
            # keep track of which components have finished
            probeComponents = probe.components
            for thisComponent in probe.components:
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
            
            # --- Run Routine "probe" ---
            thisExp.currentRoutine = probe
            probe.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 3.3:
                # if trial has changed, end Routine now
                if hasattr(thisSFT_5, 'status') and thisSFT_5.status == STOPPING:
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
                    if tThisFlipGlobal > Fixation.tStartRefresh + .3-frameTolerance:
                        # keep track of stop time/frame for later
                        Fixation.tStop = t  # not accounting for scr refresh
                        Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        Fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Fixation.stopped')
                        # update status
                        Fixation.status = FINISHED
                        Fixation.setAutoDraw(False)
                
                # *targetV* updates
                
                # if targetV is starting this frame...
                if targetV.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetV.frameNStart = frameN  # exact frame index
                    targetV.tStart = t  # local t and not account for scr refresh
                    targetV.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(targetV, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetV.started')
                    # update status
                    targetV.status = STARTED
                    targetV.setAutoDraw(True)
                
                # if targetV is active this frame...
                if targetV.status == STARTED:
                    # update params
                    pass
                
                # if targetV is stopping this frame...
                if targetV.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetV.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        targetV.tStop = t  # not accounting for scr refresh
                        targetV.tStopRefresh = tThisFlipGlobal  # on global time
                        targetV.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetV.stopped')
                        # update status
                        targetV.status = FINISHED
                        targetV.setAutoDraw(False)
                
                # *targetA* updates
                
                # if targetA is starting this frame...
                if targetA.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetA.frameNStart = frameN  # exact frame index
                    targetA.tStart = t  # local t and not account for scr refresh
                    targetA.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('targetA.started', tThisFlipGlobal)
                    # update status
                    targetA.status = STARTED
                    targetA.play(when=win)  # sync with win flip
                
                # if targetA is stopping this frame...
                if targetA.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetA.tStartRefresh + 1-frameTolerance or targetA.isFinished:
                        # keep track of stop time/frame for later
                        targetA.tStop = t  # not accounting for scr refresh
                        targetA.tStopRefresh = tThisFlipGlobal  # on global time
                        targetA.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetA.stopped')
                        # update status
                        targetA.status = FINISHED
                        targetA.stop()
                # *ResponseBox* updates
                
                # if ResponseBox is starting this frame...
                if ResponseBox.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    ResponseBox.frameNStart = frameN  # exact frame index
                    ResponseBox.tStart = t  # local t and not account for scr refresh
                    ResponseBox.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ResponseBox, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    ResponseBox.status = STARTED
                    ResponseBox.clock.reset()  # now t=0
                    # clear keyboard responses
                    ResponseBox.keys = []
                    ResponseBox.rt = []
                    ResponseBox.clearEvents(eventType='keyboard')
                
                # if ResponseBox is stopping this frame...
                if ResponseBox.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ResponseBox.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        ResponseBox.tStop = t  # not accounting for scr refresh
                        ResponseBox.tStopRefresh = tThisFlipGlobal  # on global time
                        ResponseBox.frameNStop = frameN  # exact frame index
                        # update status
                        ResponseBox.status = FINISHED
                if ResponseBox.status == STARTED:
                    # check for key presses using keyboard
                    theseKeys = ResponseBox.getKeys(keyList=['y', 'n'], ignoreKeys=["escape"], waitRelease=False)
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if ResponseBox.keys == []:  # then this is first keypress
                            ResponseBox.keys = theseKeys[0].name  # 'y' or 'n'
                            ResponseBox.rt = theseKeys[0].rt
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
                        currentRoutine=probe,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    probe.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if probe.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in probe.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "probe" ---
            for thisComponent in probe.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for probe
            probe.tStop = globalClock.getTime(format='float')
            probe.tStopRefresh = tThisFlipGlobal
            thisExp.addData('probe.stopped', probe.tStop)
            # Run 'End Routine' code from ProbeCode
            # Check if the hardware was actually found and a response was made
            #if ResponseBox is not None and hasattr(ResponseBox, 'duration'):
            #    if ResponseBox.duration is not None:
            #        thisExp.addData('ResponseBox.duration', ResponseBox.duration)
            # Check if the hardware was initialized and a response occurred
            if ResponseBox is not None:
                # Use getattr to safely check for 'duration' without crashing
                resp_dur = getattr(ResponseBox, 'duration', None)
                if resp_dur is not None:
                    thisExp.addData('ResponseBox.duration', resp_dur)
                else:
                    thisExp.addData('ResponseBox.duration', 'no_response')
            else:
                thisExp.addData('ResponseBox.duration', 'device_not_found')
            thisExp.addData('condition', condition)
            thisExp.addData('TargetA', targetAud)
            thisExp.addData('TargetC', targetCol)
            
            targetA.pause()  # ensure sound has stopped at end of Routine
            # check responses
            if ResponseBox.keys in ['', [], None]:  # No response was made
                ResponseBox.keys = None
            SFT_5.addData('ResponseBox.keys',ResponseBox.keys)
            if ResponseBox.keys != None:  # we had a response
                SFT_5.addData('ResponseBox.rt', ResponseBox.rt)
            #    SFT_5.addData('ResponseBox.duration', ResponseBox.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if probe.maxDurationReached:
                routineTimer.addTime(-probe.maxDuration)
            elif probe.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-3.300000)
            # mark thisSFT_5 as finished
            if hasattr(thisSFT_5, 'status'):
                thisSFT_5.status = FINISHED
            # if awaiting a pause, pause now
            if SFT_5.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                SFT_5.status = STARTED
            thisExp.nextEntry()
            
        # completed 9 repeats of 'SFT_5'
        SFT_5.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisBlock5 as finished
        if hasattr(thisBlock5, 'status'):
            thisBlock5.status = FINISHED
        # if awaiting a pause, pause now
        if block5.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            block5.status = STARTED
        thisExp.nextEntry()
        
    # completed 25 repeats of 'block5'
    block5.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "rest" ---
    # create an object to store info about Routine rest
    rest = data.Routine(
        name='rest',
        components=[timeout, breakend],
    )
    rest.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for breakend
    breakend.keys = []
    breakend.rt = []
    _breakend_allKeys = []
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
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *timeout* updates
        
        # if timeout is starting this frame...
        if timeout.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            timeout.frameNStart = frameN  # exact frame index
            timeout.tStart = t  # local t and not account for scr refresh
            timeout.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(timeout, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'timeout.started')
            # update status
            timeout.status = STARTED
            timeout.setAutoDraw(True)
        
        # if timeout is active this frame...
        if timeout.status == STARTED:
            # update params
            pass
        
        # *breakend* updates
        waitOnFlip = False
        
        # if breakend is starting this frame...
        if breakend.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            breakend.frameNStart = frameN  # exact frame index
            breakend.tStart = t  # local t and not account for scr refresh
            breakend.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(breakend, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'breakend.started')
            # update status
            breakend.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(breakend.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(breakend.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if breakend.status == STARTED and not waitOnFlip:
            theseKeys = breakend.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _breakend_allKeys.extend(theseKeys)
            if len(_breakend_allKeys):
                breakend.keys = _breakend_allKeys[-1].name  # just the last key pressed
                breakend.rt = _breakend_allKeys[-1].rt
                breakend.duration = _breakend_allKeys[-1].duration
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
    # check responses
    if breakend.keys in ['', [], None]:  # No response was made
        breakend.keys = None
    thisExp.addData('breakend.keys',breakend.keys)
    if breakend.keys != None:  # we had a response
        thisExp.addData('breakend.rt', breakend.rt)
        thisExp.addData('breakend.duration', breakend.duration)
    thisExp.nextEntry()
    # the Routine "rest" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    block6 = data.TrialHandler2(
        name='block6',
        nReps=1, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=45, 
        isTrials=True, 
    )
    thisExp.addLoop(block6)  # add the loop to the experiment
    thisBlock6 = block6.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock6.rgb)
    if thisBlock6 != None:
        for paramName in thisBlock6:
            globals()[paramName] = thisBlock6[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock6 in block6:
        block6.status = STARTED
        if hasattr(thisBlock6, 'status'):
            thisBlock6.status = STARTED
        currentLoop = block6
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock6.rgb)
        if thisBlock6 != None:
            for paramName in thisBlock6:
                globals()[paramName] = thisBlock6[paramName]
        
        # --- Prepare to start Routine "study_stage" ---
        # create an object to store info about Routine study_stage
        study_stage = data.Routine(
            name='study_stage',
            components=[Fix, stim1, stim2, audi1, audi2],
        )
        study_stage.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # Run 'Begin Routine' code from StudyCode
        
        
        stim1.setFillColor(color1_target)
        stim1.setOpacity(1.0)
        stim1.setPos((-200, 0))
        stim2.setFillColor(color2_target)
        stim2.setOpacity(None)
        stim2.setPos((200,0))
        audi1.setSound(audio1_target_file, secs=1, hamming=True)
        audi1.setVolume(1.0, log=False)
        audi1.seek(0)
        audi2.setSound(audio2_target_file, secs=1, hamming=True)
        audi2.setVolume(1.0, log=False)
        audi2.seek(0)
        # store start times for study_stage
        study_stage.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        study_stage.tStart = globalClock.getTime(format='float')
        study_stage.status = STARTED
        thisExp.addData('study_stage.started', study_stage.tStart)
        study_stage.maxDuration = None
        # keep track of which components have finished
        study_stageComponents = study_stage.components
        for thisComponent in study_stage.components:
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
        
        # --- Run Routine "study_stage" ---
        thisExp.currentRoutine = study_stage
        study_stage.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 4.3:
            # if trial has changed, end Routine now
            if hasattr(thisBlock6, 'status') and thisBlock6.status == STOPPING:
                continueRoutine = False
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *Fix* updates
            
            # if Fix is starting this frame...
            if Fix.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                Fix.frameNStart = frameN  # exact frame index
                Fix.tStart = t  # local t and not account for scr refresh
                Fix.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(Fix, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'Fix.started')
                # update status
                Fix.status = STARTED
                Fix.setAutoDraw(True)
            
            # if Fix is active this frame...
            if Fix.status == STARTED:
                # update params
                pass
            
            # if Fix is stopping this frame...
            if Fix.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > Fix.tStartRefresh + .3-frameTolerance:
                    # keep track of stop time/frame for later
                    Fix.tStop = t  # not accounting for scr refresh
                    Fix.tStopRefresh = tThisFlipGlobal  # on global time
                    Fix.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'Fix.stopped')
                    # update status
                    Fix.status = FINISHED
                    Fix.setAutoDraw(False)
            
            # *stim1* updates
            
            # if stim1 is starting this frame...
            if stim1.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                # keep track of start time/frame for later
                stim1.frameNStart = frameN  # exact frame index
                stim1.tStart = t  # local t and not account for scr refresh
                stim1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim1.started')
                # update status
                stim1.status = STARTED
                stim1.setAutoDraw(True)
            
            # if stim1 is active this frame...
            if stim1.status == STARTED:
                # update params
                pass
            
            # if stim1 is stopping this frame...
            if stim1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim1.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim1.tStop = t  # not accounting for scr refresh
                    stim1.tStopRefresh = tThisFlipGlobal  # on global time
                    stim1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim1.stopped')
                    # update status
                    stim1.status = FINISHED
                    stim1.setAutoDraw(False)
            
            # *stim2* updates
            
            # if stim2 is starting this frame...
            if stim2.status == NOT_STARTED and tThisFlip >= 1.3-frameTolerance:
                # keep track of start time/frame for later
                stim2.frameNStart = frameN  # exact frame index
                stim2.tStart = t  # local t and not account for scr refresh
                stim2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(stim2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stim2.started')
                # update status
                stim2.status = STARTED
                stim2.setAutoDraw(True)
            
            # if stim2 is active this frame...
            if stim2.status == STARTED:
                # update params
                pass
            
            # if stim2 is stopping this frame...
            if stim2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > stim2.tStartRefresh + 1-frameTolerance:
                    # keep track of stop time/frame for later
                    stim2.tStop = t  # not accounting for scr refresh
                    stim2.tStopRefresh = tThisFlipGlobal  # on global time
                    stim2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'stim2.stopped')
                    # update status
                    stim2.status = FINISHED
                    stim2.setAutoDraw(False)
            
            # *audi1* updates
            
            # if audi1 is starting this frame...
            if audi1.status == NOT_STARTED and tThisFlip >= 2.3-frameTolerance:
                # keep track of start time/frame for later
                audi1.frameNStart = frameN  # exact frame index
                audi1.tStart = t  # local t and not account for scr refresh
                audi1.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi1.started', tThisFlipGlobal)
                # update status
                audi1.status = STARTED
                audi1.play(when=win)  # sync with win flip
            
            # if audi1 is stopping this frame...
            if audi1.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi1.tStartRefresh + 1-frameTolerance or audi1.isFinished:
                    # keep track of stop time/frame for later
                    audi1.tStop = t  # not accounting for scr refresh
                    audi1.tStopRefresh = tThisFlipGlobal  # on global time
                    audi1.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi1.stopped')
                    # update status
                    audi1.status = FINISHED
                    audi1.stop()
            
            # *audi2* updates
            
            # if audi2 is starting this frame...
            if audi2.status == NOT_STARTED and tThisFlip >= 3.3-frameTolerance:
                # keep track of start time/frame for later
                audi2.frameNStart = frameN  # exact frame index
                audi2.tStart = t  # local t and not account for scr refresh
                audi2.tStartRefresh = tThisFlipGlobal  # on global time
                # add timestamp to datafile
                thisExp.addData('audi2.started', tThisFlipGlobal)
                # update status
                audi2.status = STARTED
                audi2.play(when=win)  # sync with win flip
            
            # if audi2 is stopping this frame...
            if audi2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > audi2.tStartRefresh + 1-frameTolerance or audi2.isFinished:
                    # keep track of stop time/frame for later
                    audi2.tStop = t  # not accounting for scr refresh
                    audi2.tStopRefresh = tThisFlipGlobal  # on global time
                    audi2.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'audi2.stopped')
                    # update status
                    audi2.status = FINISHED
                    audi2.stop()
            
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
                    currentRoutine=study_stage,
                )
                # skip the frame we paused on
                continue
            
            # has a Component requested the Routine to end?
            if not continueRoutine:
                study_stage.forceEnded = routineForceEnded = True
            # has the Routine been forcibly ended?
            if study_stage.forceEnded or routineForceEnded:
                break
            # has every Component finished?
            continueRoutine = False
            for thisComponent in study_stage.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "study_stage" ---
        for thisComponent in study_stage.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for study_stage
        study_stage.tStop = globalClock.getTime(format='float')
        study_stage.tStopRefresh = tThisFlipGlobal
        thisExp.addData('study_stage.stopped', study_stage.tStop)
        audi1.pause()  # ensure sound has stopped at end of Routine
        audi2.pause()  # ensure sound has stopped at end of Routine
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if study_stage.maxDurationReached:
            routineTimer.addTime(-study_stage.maxDuration)
        elif study_stage.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-4.300000)
        
        # set up handler to look after randomisation of conditions etc
        SFT_6 = data.TrialHandler2(
            name='SFT_6',
            nReps=9,
            method='random',
            extraInfo=expInfo,
            originPath=-1,
            trialList=[None],
            seed=None,
            isTrials=True,
        )
        # Generate stratified conditions for this block
        probe_conditions = generate_stratified_conditions()
        probe_idx = 0
        thisExp.addLoop(SFT_6)  # add the loop to the experiment
        thisSFT_6 = SFT_6.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisSFT_6.rgb)
        if thisSFT_6 != None:
            for paramName in thisSFT_6:
                globals()[paramName] = thisSFT_6[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisSFT_6 in SFT_6:
            SFT_6.status = STARTED
            if hasattr(thisSFT_6, 'status'):
                thisSFT_6.status = STARTED
            currentLoop = SFT_6
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisSFT_6.rgb)
            if thisSFT_6 != None:
                for paramName in thisSFT_6:
                    globals()[paramName] = thisSFT_6[paramName]

            # --- Prepare to start Routine "probe" ---
            # create an object to store info about Routine probe
            probe = data.Routine(
                name='probe',
                components=[Fixation, targetV, targetA, ResponseBox],
            )
            probe.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from ProbeCode
            # Use pre-generated stratified condition
            condition = probe_conditions[probe_idx]
            probe_idx += 1
            # Old random code removed - now using stratified conditions
            #AX AX= color, XA= audio
            #AA=0 HA =1 LA = 2
            #AH=3 HH=4 LH=5
            #AL=6 HL=7 LL=8
            if condition == 0 :#AA .25
               targetCol = color1_target
               targetAud = audio1_target_file
            elif condition == 1:#AA.25
                targetCol = color2_target
                targetAud = audio2_target_file
            if condition == 2:#HA
               targetCol = color1_target
               targetAud = audio1_H_file
            elif condition == 3:#HA
                targetCol = color2_target
                targetAud = audio2_H_file
            if condition == 4:#LA
               targetCol = color1_target
               targetAud = audio1_L_file
            elif condition == 5:#LA
                targetCol = color2_target
                targetAud = audio2_L_file
            if condition == 6:#AH
               targetCol = color1_H
               targetAud = audio1_target_file
            elif condition == 7:#AH
                targetCol = color2_H
                targetAud = audio2_target_file
            if condition == 8:#HH
               targetCol = color1_H
               targetAud = audio1_H_file
            elif condition == 9:#HH
                targetCol = color2_H
                targetAud = audio2_H_file
            if condition == 10:#LH
               targetCol = color1_L
               targetAud = audio1_H_file
            elif condition == 11:#LH
                targetCol = color2_L
                targetAud = audio2_H_file
            if condition == 12: #AL
               targetCol = color1_L
               targetAud = audio1_target_file
            elif condition == 13: #AL
                targetCol = color2_L
                targetAud = audio2_target_file
            if condition == 14:#HL
               targetCol = color1_H
               targetAud = audio1_L_file
            elif condition == 15:#HL
                targetCol = color2_H
                targetAud = audio2_L_file
            if condition == 16:#LL
               targetCol = color1_L
               targetAud = audio1_L_file
            elif condition == 17:#LL
                targetCol = color2_L
                targetAud = audio2_L_file
            
            targetV.setFillColor(targetCol)
            targetV.setPos((0,0))
            targetA.setSound(targetAud, secs=1, hamming=True)
            targetA.setVolume(1.0, log=False)
            targetA.seek(0)
            ResponseBox.keys = []  # to store response values
            ResponseBox.rt = []
            ResponseBox.status = NOT_STARTED
            # store start times for probe
            probe.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            probe.tStart = globalClock.getTime(format='float')
            probe.status = STARTED
            thisExp.addData('probe.started', probe.tStart)
            probe.maxDuration = None
            # keep track of which components have finished
            probeComponents = probe.components
            for thisComponent in probe.components:
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
            
            # --- Run Routine "probe" ---
            thisExp.currentRoutine = probe
            probe.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine and routineTimer.getTime() < 3.3:
                # if trial has changed, end Routine now
                if hasattr(thisSFT_6, 'status') and thisSFT_6.status == STOPPING:
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
                    if tThisFlipGlobal > Fixation.tStartRefresh + .3-frameTolerance:
                        # keep track of stop time/frame for later
                        Fixation.tStop = t  # not accounting for scr refresh
                        Fixation.tStopRefresh = tThisFlipGlobal  # on global time
                        Fixation.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'Fixation.stopped')
                        # update status
                        Fixation.status = FINISHED
                        Fixation.setAutoDraw(False)
                
                # *targetV* updates
                
                # if targetV is starting this frame...
                if targetV.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetV.frameNStart = frameN  # exact frame index
                    targetV.tStart = t  # local t and not account for scr refresh
                    targetV.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(targetV, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'targetV.started')
                    # update status
                    targetV.status = STARTED
                    targetV.setAutoDraw(True)
                
                # if targetV is active this frame...
                if targetV.status == STARTED:
                    # update params
                    pass
                
                # if targetV is stopping this frame...
                if targetV.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetV.tStartRefresh + 1-frameTolerance:
                        # keep track of stop time/frame for later
                        targetV.tStop = t  # not accounting for scr refresh
                        targetV.tStopRefresh = tThisFlipGlobal  # on global time
                        targetV.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetV.stopped')
                        # update status
                        targetV.status = FINISHED
                        targetV.setAutoDraw(False)
                
                # *targetA* updates
                
                # if targetA is starting this frame...
                if targetA.status == NOT_STARTED and tThisFlip >= .3-frameTolerance:
                    # keep track of start time/frame for later
                    targetA.frameNStart = frameN  # exact frame index
                    targetA.tStart = t  # local t and not account for scr refresh
                    targetA.tStartRefresh = tThisFlipGlobal  # on global time
                    # add timestamp to datafile
                    thisExp.addData('targetA.started', tThisFlipGlobal)
                    # update status
                    targetA.status = STARTED
                    targetA.play(when=win)  # sync with win flip
                
                # if targetA is stopping this frame...
                if targetA.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > targetA.tStartRefresh + 1-frameTolerance or targetA.isFinished:
                        # keep track of stop time/frame for later
                        targetA.tStop = t  # not accounting for scr refresh
                        targetA.tStopRefresh = tThisFlipGlobal  # on global time
                        targetA.frameNStop = frameN  # exact frame index
                        # add timestamp to datafile
                        thisExp.timestampOnFlip(win, 'targetA.stopped')
                        # update status
                        targetA.status = FINISHED
                        targetA.stop()
                # *ResponseBox* updates
                
                # if ResponseBox is starting this frame...
                if ResponseBox.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                    # keep track of start time/frame for later
                    ResponseBox.frameNStart = frameN  # exact frame index
                    ResponseBox.tStart = t  # local t and not account for scr refresh
                    ResponseBox.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(ResponseBox, 'tStartRefresh')  # time at next scr refresh
                    # update status
                    ResponseBox.status = STARTED
                    ResponseBox.clock.reset()  # now t=0
                    # clear keyboard responses
                    ResponseBox.keys = []
                    ResponseBox.rt = []
                    ResponseBox.clearEvents(eventType='keyboard')
                
                # if ResponseBox is stopping this frame...
                if ResponseBox.status == STARTED:
                    # is it time to stop? (based on global clock, using actual start)
                    if tThisFlipGlobal > ResponseBox.tStartRefresh + 2-frameTolerance:
                        # keep track of stop time/frame for later
                        ResponseBox.tStop = t  # not accounting for scr refresh
                        ResponseBox.tStopRefresh = tThisFlipGlobal  # on global time
                        ResponseBox.frameNStop = frameN  # exact frame index
                        # update status
                        ResponseBox.status = FINISHED
                if ResponseBox.status == STARTED:
                    # check for key presses using keyboard
                    theseKeys = ResponseBox.getKeys(keyList=['y', 'n'], ignoreKeys=["escape"], waitRelease=False)
                    if len(theseKeys) > 0:  # at least one key was pressed
                        if ResponseBox.keys == []:  # then this is first keypress
                            ResponseBox.keys = theseKeys[0].name  # 'y' or 'n'
                            ResponseBox.rt = theseKeys[0].rt
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
                        currentRoutine=probe,
                    )
                    # skip the frame we paused on
                    continue
                
                # has a Component requested the Routine to end?
                if not continueRoutine:
                    probe.forceEnded = routineForceEnded = True
                # has the Routine been forcibly ended?
                if probe.forceEnded or routineForceEnded:
                    break
                # has every Component finished?
                continueRoutine = False
                for thisComponent in probe.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "probe" ---
            for thisComponent in probe.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for probe
            probe.tStop = globalClock.getTime(format='float')
            probe.tStopRefresh = tThisFlipGlobal
            thisExp.addData('probe.stopped', probe.tStop)
            # Run 'End Routine' code from ProbeCode
            # Check if the hardware was actually found and a response was made
            #if ResponseBox is not None and hasattr(ResponseBox, 'duration'):
            #    if ResponseBox.duration is not None:
            #        thisExp.addData('ResponseBox.duration', ResponseBox.duration)
            # Check if the hardware was initialized and a response occurred
            if ResponseBox is not None:
                # Use getattr to safely check for 'duration' without crashing
                resp_dur = getattr(ResponseBox, 'duration', None)
                if resp_dur is not None:
                    thisExp.addData('ResponseBox.duration', resp_dur)
                else:
                    thisExp.addData('ResponseBox.duration', 'no_response')
            else:
                thisExp.addData('ResponseBox.duration', 'device_not_found')
            thisExp.addData('condition', condition)
            thisExp.addData('TargetA', targetAud)
            thisExp.addData('TargetC', targetCol)
            
            targetA.pause()  # ensure sound has stopped at end of Routine
            # check responses
            if ResponseBox.keys in ['', [], None]:  # No response was made
                ResponseBox.keys = None
            SFT_6.addData('ResponseBox.keys',ResponseBox.keys)
            if ResponseBox.keys != None:  # we had a response
                SFT_6.addData('ResponseBox.rt', ResponseBox.rt)
            #    SFT_6.addData('ResponseBox.duration', ResponseBox.duration)
            # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
            if probe.maxDurationReached:
                routineTimer.addTime(-probe.maxDuration)
            elif probe.forceEnded:
                routineTimer.reset()
            else:
                routineTimer.addTime(-3.300000)
            # mark thisSFT_6 as finished
            if hasattr(thisSFT_6, 'status'):
                thisSFT_6.status = FINISHED
            # if awaiting a pause, pause now
            if SFT_6.status == PAUSED:
                thisExp.status = PAUSED
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[globalClock], 
                )
                # once done pausing, restore running status
                SFT_6.status = STARTED
            thisExp.nextEntry()
            
        # completed 9 repeats of 'SFT_6'
        SFT_6.status = FINISHED
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # mark thisBlock6 as finished
        if hasattr(thisBlock6, 'status'):
            thisBlock6.status = FINISHED
        # if awaiting a pause, pause now
        if block6.status == PAUSED:
            thisExp.status = PAUSED
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[globalClock], 
            )
            # once done pausing, restore running status
            block6.status = STARTED
        thisExp.nextEntry()
        
    # completed 25 repeats of 'block6'
    block6.status = FINISHED
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "End" ---
    # create an object to store info about Routine End
    End = data.Routine(
        name='End',
        components=[EndExp, callExp],
    )
    End.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for callExp
    callExp.keys = []
    callExp.rt = []
    _callExp_allKeys = []
    # store start times for End
    End.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    End.tStart = globalClock.getTime(format='float')
    End.status = STARTED
    thisExp.addData('End.started', End.tStart)
    End.maxDuration = None
    # keep track of which components have finished
    EndComponents = End.components
    for thisComponent in End.components:
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
    
    # --- Run Routine "End" ---
    thisExp.currentRoutine = End
    End.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *EndExp* updates
        
        # if EndExp is starting this frame...
        if EndExp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            EndExp.frameNStart = frameN  # exact frame index
            EndExp.tStart = t  # local t and not account for scr refresh
            EndExp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(EndExp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'EndExp.started')
            # update status
            EndExp.status = STARTED
            EndExp.setAutoDraw(True)
        
        # if EndExp is active this frame...
        if EndExp.status == STARTED:
            # update params
            pass
        
        # *callExp* updates
        waitOnFlip = False
        
        # if callExp is starting this frame...
        if callExp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            callExp.frameNStart = frameN  # exact frame index
            callExp.tStart = t  # local t and not account for scr refresh
            callExp.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(callExp, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'callExp.started')
            # update status
            callExp.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(callExp.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(callExp.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if callExp.status == STARTED and not waitOnFlip:
            theseKeys = callExp.getKeys(keyList=['space'], ignoreKeys=["escape"], waitRelease=False)
            _callExp_allKeys.extend(theseKeys)
            if len(_callExp_allKeys):
                callExp.keys = _callExp_allKeys[-1].name  # just the last key pressed
                callExp.rt = _callExp_allKeys[-1].rt
                callExp.duration = _callExp_allKeys[-1].duration
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
                currentRoutine=End,
            )
            # skip the frame we paused on
            continue
        
        # has a Component requested the Routine to end?
        if not continueRoutine:
            End.forceEnded = routineForceEnded = True
        # has the Routine been forcibly ended?
        if End.forceEnded or routineForceEnded:
            break
        # has every Component finished?
        continueRoutine = False
        for thisComponent in End.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "End" ---
    for thisComponent in End.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for End
    End.tStop = globalClock.getTime(format='float')
    End.tStopRefresh = tThisFlipGlobal
    thisExp.addData('End.stopped', End.tStop)
    # check responses
    if callExp.keys in ['', [], None]:  # No response was made
        callExp.keys = None
    thisExp.addData('callExp.keys',callExp.keys)
    if callExp.keys != None:  # we had a response
        thisExp.addData('callExp.rt', callExp.rt)
        thisExp.addData('callExp.duration', callExp.duration)
    thisExp.nextEntry()
    # the Routine "End" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
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
