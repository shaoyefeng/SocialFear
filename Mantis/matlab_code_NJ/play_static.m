%% play static
Screen('PlayMovie', movie, 0);
tex = Screen('GetMovieImage', win, movie, [], 0);
t_static_start = toc;
fprintf(stim_out, 'static_start %.3f\n', t_static_start);

while 1
    [keyIsDown,~,keyCode] = KbCheck;
    if (keyIsDown==1 && keyCode(esc))
        exit = 1;
        break;
    end
    for x=video_offset_x:(video_w+video_x_inter):screen_width_pix
        if x+video_w > screen_width_pix
            break;
        end
        Screen('DrawTexture', win, tex, [], [x video_offset_y x+video_w video_offset_y+video_h]);
    end
    Screen('Flip', win);
    dt = toc-t_static_start;
    if dt > video_interval
        break;
    end
end
fprintf(stim_out, 'static_end %.3f\n', toc);