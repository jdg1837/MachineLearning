function [accuracy, confusion_matrix] = nnc_chamfer_stats()
    accuracy = 0;
    confusion_matrix = zeros(10,10);
    for x = 0:9
        for y = 1:10
            test_file = sprintf('digits_test/label%d_test%d.png', x, y);
            test_image = imread(test_file);
            class = nnc_chamfer(test_image);
            if x == class
                accuracy = accuracy + 1;
            end
            i = x;
            if i == 0
                i = 10;
            end
            j = class;
            if j == 0
                j = 10;
            end
            confusion_matrix(i,j) = confusion_matrix(i,j) + 1;
        end
    end
    accuracy = accuracy/100;
    confusion_matrix = confusion_matrix ./ 10;
end