# Write the integer value 1 to current frame.
.w 1

# Increment tape.
+

# Write the sum of t1 and t2 to current frame
.w t1 + t2 

# Execute the above instructions on one line.
.w 1 + .w 1 + .w .calc t1 + t2

# Specify and name sequence above as a region
.r .n add .w 1  + .w 1  + .w .calc t1 + t2

# Or like this with auto increment on (* +):
# (tape increments 1 frame after each write)

.r .n add *+ .w 1 .w 1 .w .calc t1 + t2

# Or like this, using auto increment and auto write.
.r .n add *+ *.w  1 1 .calc t1 + t2


