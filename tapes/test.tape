# Write the integer value 1 to current frame.
.w 1

# Read the value in current frame.
.r

# Increment tape.
+

# Write the sum of t1 and t2 to current frame
.w t1 + t2 

# Execute the above instructions on one line.
.w 1 + .w 1 + .w .calc t1 + t2

# Specify and name these instructions as a segment.
.s .n add .w 1  + .w 1  + .w .calc t1 + t2

# Or like this with auto increment on (* +):
# (tape increments 1 frame after each write)

.s .n add *+ .w 1 .w 1 .w .calc t1 + t2

# Or like this, using auto increment and auto write.
.s .n add *+ *.w  1 1 .calc t1 + t2


