function class_label = nnc_euclidean(test_image)
    min = Inf;
    class_label = -1;
    for x = 0:9
        for y = 1:15
            training_file = sprintf('digits_training/label%d_training%d.png', x, y);
            training_image = imread(training_file);
            distance = euclidean_distance(test_image,training_image);
            if distance < min
                min = distance;
                class_label = x;
            end
        end
    end     
end