**Project Idea List**

1. Mesh Network - grab a few ChipSats and write radio transmit and recieve code to create a mesh network of these ChipSats. 
   - https://libremesh.org/
   - https://people.eecs.berkeley.edu/~pister/publications/2012/openwsnETT.pdf
2. Make a plotter that injects ChipSats into optimal orbits based on other debris/satellites.
   1. Visit the Resources and Two-Line Visualizer docs for usueful info on this.
3. Explore ML/RL approaches for manuevering the ChipSats. - Useful info in python files within this repo.
   1. Implement in scikit learn or pytourch and then convert to TensorFlow and then to TF Lite.
   2. Make a simple Tensorflow Lite ML approach to analyze the data on one of the sensors on the ChipSat.
      1. TF Lite can do basic RL models - but not much as of right now.
      2. Has a great image model - attach camera to ChipSat and use TF Lite to process image data as a way to get the pose of the ChipSat by looking at the Stars or Earth.
4. 

