function directed_distance = directed_chamfer(image1, image2)
    v1_binary = (image1 ~= 0);
    n1 = sum(sum(v1_binary));
    dt2 = bwdist(image2);
    directed_distance = sum(sum(v1_binary .* dt2));
    directed_distance = directed_distance/n1;
end