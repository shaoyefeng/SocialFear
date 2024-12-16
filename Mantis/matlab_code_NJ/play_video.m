%% play video
Screen('PlayMovie', movie, 1);
fprintf(stim_out, 'video_start %.3f\n', toc);

while 1
    [keyIsDown,~,keyCode] = KbCheck;
    if (keyIsDown==1 && keyCode(esc))
        exit = 1;
        break;
    end
    tex = Screen('GetMovieImage', win, movie);
    if tex<=0
        break;
    end
%     Screen('DrawTexture', win, tex, [], [0 0 video_w video_h]);
%     Screen('DrawTexture', win, tex, [], [video_w 0 video_w*2 video_h]);
    for x=video_offset_x:(video_w+video_x_inter):screen_width_pix
        if x+video_w > screen_width_pix
            break;
        end
        Screen('DrawTexture', win, tex, [], [x video_offset_y x+video_w video_offset_y+video_h]);
    end
    Screen('Flip', win);
    Screen('Close', tex);
end
fprintf(stim_out, 'video_end %.3f\n', toc);