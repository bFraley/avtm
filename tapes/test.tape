# Name a segment called 'start' that begins at frame 0.
.s .n start

# Write the value 1 to this frame.
.w 1

# Increment tape
+

# Write the value 'hello' to frame.
.w hello

# Read value of current frame.
.r

# Increment and write 'world' to frame.
+
.w world

# Read value of frame 0, and read value of frame 1
.r 0
.r 1

# Increment and name the frame 'myframe', write 'this is my frame!'
+
.n myframe
.w this is my frame!

# Read the value of frame named myframe.
.r myframe

# Inspect the current machine state data.
.i

