SELECT id, mergelist, min_x, min_y
  FROM gs_bbox_grid
--   where mergelist = 1
  where id = 532
  order by mergelist;
