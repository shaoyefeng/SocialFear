clc
clear 
close all

%video_duration = 5; % s
video_interval = 30; % s (first frame)
bout_video_n = 5; % n 5*60
bout_interval = 1500; % s 25*60 (random)
bout_n = 2; % n
video_w = 300; % pix
video_h = 200; % pix
video_offset_x = 20; % pix
video_offset_y = 140; % pix
video_x_inter = 10; % pix
video_path = 'D:\OpenLoop\c.avi_vflip.mp4';
random_tex_path = 'D:\OpenLoop\c.avi_short.mp4.png';
mias_path = 'D:\mias\multi_cam.exe';
log_path = ['D:\OpenLoop\avi\' datestr(now,'yyyymmdd_HHMMSS') '.log'];

stim_out = fopen(log_path, 'w');
screen_ini_led
esc = KbName('ESCAPE');
random_tex = Screen('MakeTexture', win, imread(random_tex_path));

% Screen PlayMovie?
movie = Screen('OpenMovie', win, video_path);

%Screen('FillRect', win, [0 0 0], [0 0 screen_width_pix screen_height_pix]);
play_random_inter
exit = 0;
%% loop
for bout_i=1:bout_n
    t_start = now;
    tic;
    fprintf(stim_out, 'START %.3f %s\n', (t_start-datenum(1970,1,1))*86400-8*3600, datestr(t_start, 'yyyymmdd_HHMMSS'));
    system(['start ' mias_path]);
    pause(5);
    
    for video_i=1:bout_video_n
        disp(['bout:' num2str(bout_i) ' trial:' num2str(video_i)])
        play_video
        if exit
            break;
        end
        play_static
        if exit
            break;
        end
    end
    
    if ~exit
        play_random
    end
    
    system('taskkill /im multi_cam.exe');
    %Screen('FillRect', win, [0 0 0], [0 0 screen_width_pix screen_height_pix]);
    play_random_inter
    
    if exit
        break;
    end
    pause(10);
end

%% close
fprintf(stim_out, 'END %.3f\n', toc);
Screen('CloseMovie', movie);
fclose(stim_out);
sca;