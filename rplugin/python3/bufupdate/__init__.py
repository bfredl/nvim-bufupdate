import neovim

@neovim.plugin
class WatchPlugin(object):

    def __init__(self, nvim):
        self.nvim = nvim
        self.buffers = {}

    @neovim.command("WatchBuf")
    def startsub(self):
        self.nvim.current.buffer.api.live_updates(True)

    @neovim.rpc_export("LiveUpdateStart")
    def liveupdatestart(self, bufnr, data, more):
        data = self.buffers.get(bufnr, []) + data
        self.buffers[bufnr] = data

        if not more:
            self.on_update(bufnr, data, 0, -1)


    @neovim.rpc_export("LiveUpdate")
    def liveupdate(self, bufnr, first, num, data):
        self.buffers[bufnr][first:first+num] = data
        self.on_update(bufnr, self.buffers[bufnr], first, len(data))

    @neovim.rpc_export("LiveUpdateEnd")
    def liveupdateend(self, bufnr):
        del self.buffers[bufnr]
        #TODO: event also here

    def on_update(self, bufnr, data, first, num):
        pass

    @neovim.function("WatchDebug", sync=True)
    def debug(self, args):
        return {str(k):v for (k,v) in self.buffers.items()}





