function distance = chamfer_distance(image1, image2)
    c1 = directed_chamfer(image1, image2);
    c2 = directed_chamfer(image2, image1);
    distance = c1 + c2;
end