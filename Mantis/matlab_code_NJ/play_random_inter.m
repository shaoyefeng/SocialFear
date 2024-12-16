 for x=video_offset_x:(video_w+video_x_inter):screen_width_pix
    if x+video_w > screen_width_pix
        break;
    end
    Screen('DrawTexture', win, random_tex, [], [x video_offset_y x+video_w video_offset_y+video_h]);
end
Screen('Flip', win);