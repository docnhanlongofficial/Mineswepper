


import javax.sound.sampled.*;
import java.io.IOException;



public class Sound {

    public static synchronized void playSound(final String strPath) {
        new Thread(new Runnable() {
            public void run() {
                try {
                    Clip clp = AudioSystem.getClip();

                    AudioInputStream aisStream =
                            AudioSystem.getAudioInputStream(Sound.class.getResourceAsStream(strPath));


                    clp.open(aisStream);
                    clp.start();
                } catch (Exception e) {
                    System.err.println(e.getMessage());
                }
            }
        }).start();
    }

    public static Clip clipForLoopFactory(String strPath) {

        Clip clp = null;


        try {
            AudioInputStream aisStream =
                    AudioSystem.getAudioInputStream(Sound.class.getResourceAsStream(strPath));
            clp = AudioSystem.getClip();
            clp.open(aisStream);

        } catch (UnsupportedAudioFileException exp) {

            exp.printStackTrace();
        } catch (IOException exp) {

            exp.printStackTrace();
        } catch (LineUnavailableException exp) {

            exp.printStackTrace();

        } catch (Exception exp) {
            System.out.println("error");
        }

        return clp;

    }
    public static void stopLoopingSounds(Clip... clpClips) {
        for (Clip clp : clpClips) {
            clp.stop();
        }
    }
}