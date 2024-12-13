import pyxel


class MusicMainGame:
    def music_start(self):
        pyxel.sounds[0].set(
            "E3E3 B2 C3 D3D3 C3 B2 A2A2 A2 C3 E3E3 D3 C3 B2B2 B2 C3 D3D3 E3E3 C3C3 A2A2 A2A2 RR"  "R D3D3 F3 A3A3 G3 F3 E3E3 R C3 E3E3 D3 C3 B2B2 B2 C3 D3D3 E3E3 C3C3 A2A2 A2A2 RR",
            "p",
            "5",
            "v",
            30,
        )

        pyxel.sounds[1].set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1" "a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t",
            "3",
            "n",
            30,
        )
        pyxel.sounds[2].set(
            "f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "6622 6622 6622 6422", "f", 30
        )
        pyxel.play(0, [0], loop=True)
        pyxel.play(1, [1], loop=True)
        pyxel.play(2, [2], loop=True)

    def sound_effect(self,idx):
        if idx==0:
            pyxel.sounds[3].set(
                "f4 b4 a4",
                "p",
                "6",
                "n",
                15
            )
        elif idx == 1:
            pyxel.sounds[3].set(
                "b3 d4 g4 b4",
                "p",
                "6",
                "n",
                15
            )
        elif idx == 2:
            pyxel.sounds[3].set(
                "e1",
                "n",
                "6",
                "n",
                15
            )
        pyxel.play(3, [3], loop=False)

    def sound_gameover(self):
        pyxel.sounds[0].set(
            "g0 g0 g0 e0e0e0 r f0 f0 f0 d0d0d0 r",
            "p",
            "6",
            "n",
            30,
        )
        pyxel.sounds[1].set(
            "g0 g0 g0 e0e0e0 r f0 f0 f0 d0d0d0 r",
            "n",
            "1",
            "n",
            30,
        )
        pyxel.play(0, [0], loop=False)
        pyxel.play(1, [1], loop=False)
        
    def music_stop(self):
        pyxel.stop(0)
        pyxel.stop(1)
        pyxel.stop(2)
