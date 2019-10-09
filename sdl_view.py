import sdl2.ext


class SdlView:

    def __init__(self, size):
        self.window = self.init_sdl(size=size)
        self.index = 0

    @staticmethod
    def init_sdl(size):
        sdl2.ext.init()
        return sdl2.ext.Window("TableScraper", size=size, position=(100, 100))

    def blit_3d_surface(self, img):
        surf = sdl2.ext.pixels3d(self.window.get_surface())
        surf[:, :, 0:3] = img.swapaxes(0, 1)
        self.window.refresh()

    def blit_2d_surface(self, img):
        surf = sdl2.ext.pixels2d(self.window.get_surface())
        surf[:, :, ] = img.swapaxes(0, 1)
        self.window.refresh()

    def handle_sdl(self, frames_2d, frames_3d):
        self.window.show()
        index = 0
        while True:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    exit(0)
                if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
                    if index == 0:
                        self.blit_3d_surface(frames_3d[0])
                        index = 1
                    elif index == 1:
                        self.blit_3d_surface(frames_3d[1])
                        index = 2
                    elif index == 2:
                        self.blit_2d_surface(frames_2d[0])
                        index = 0

            sdl2.SDL_Delay(10)

    def display_img(self, frames_3d):
        self.window.show()
        self.blit_3d_surface(frames_3d)
