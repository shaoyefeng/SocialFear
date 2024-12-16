video_path = 'D:\exp_2p\code_2p\stim\OpenLoop\c.avi_short.mp4'; 
obj = VideoReader(video_path);
%numFrames = obj.NumberOfFrames;
frame = read(obj, 1);
%imshow(frame);
imwrite(frame, [video_path '.png']);
