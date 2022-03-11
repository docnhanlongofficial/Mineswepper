import javax.sound.sampled.Clip;
import javax.swing.*;
import java.awt.*;


public class Game {

    public static final int WIDTH = 720, HEIGHT = 720;
    public static final int GRIDSIZE = 6;
    public static final int MINECOUNT = (int) Math.round(GRIDSIZE * GRIDSIZE * .1);
    public static Clip clpMusicBackground;

    private Handler handler = new Handler();

    public Game() {
        clpMusicBackground = Sound.clipForLoopFactory("src_game_sounds_plants_vs_zombies.wav");
        clpMusicBackground.loop(Clip.LOOP_CONTINUOUSLY);
        new Window(WIDTH, HEIGHT, GRIDSIZE, "Minesweeper - ", this, handler);
        Window.update(0);
    }

    public static void main(String[] args) {

        new Game();
    }
}