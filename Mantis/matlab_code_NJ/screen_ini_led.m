disp('screen_ini ...');
sca

cfg.bg_color = [0 0 0];
screen_offset_x = 2560;
screen_width_pix = 2560;
screen_height_pix = 1600;

Screen('Preference', 'SkipSyncTests', 1);
Screen('Preference', 'VisualDebuglevel', 0);
%Screen('Preference', 'Verbosity', 0);
PsychDefaultSetup(2);
%AssertOpenGL;
screens = Screen('Screens');
screenNumber = max(screens);

if screenNumber > 0
    [win, windowRect_p1] = PsychImaging('OpenWindow', 2, cfg.bg_color, [screen_offset_x 0 screen_offset_x+screen_width_pix screen_height_pix]);
else
    [win, windowRect_p1] = PsychImaging('OpenWindow', 0, cfg.bg_color, [screen_offset_x 0 screen_offset_x+screen_width_pix screen_height_pix]);
end

disp('screen_ini end.');
