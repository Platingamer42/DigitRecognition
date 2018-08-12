How were the files created? Or better:

The first model was jsut a Multilayer-Network (784-150-10); running 30 epochs - The mini_batch was 30, too.
The test-accuracy was ~98%

The second model was trained in 60 epochs used dropout-layers in addition. The accuracy was at 98.17%
The third model was trained with a changed lr (of 0.5) and an edited momentum of 0.9.  The accuracy was at 98.50%


The last and best model (yet) trained over 100 epochs, got a batch size of 20 (instead of 30) and used an edited momentum of 0.95.
The test accuracy was 98.67% Sadly, the file doesn't want to load... But thanks to this documentation, You might be able to reproduce it ;-)

(NAMES: 0123; best: only model_keras. Run "getinfo.py" for further information.)