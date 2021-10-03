class Request:
    def __init__(self, intitle, nottagged, tagged, sort, order, todate, fromdate, pagesize, page, created=None):
        self.intitle = intitle
        self.nottagged = nottagged
        self.tagged = tagged
        self.sort = sort
        self.order = order
        self.todate = todate
        self.fromdate = fromdate
        self.pagesize = pagesize
        self.page = page