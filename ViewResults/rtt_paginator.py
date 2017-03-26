from math import ceil


class RTTPaginator(object):
    default_page = 1
    default_item_count = 10
    min_item_count = 1
    # Unsigned big int (2^64)
    max_item_count = 18446744073709551615
    near_pages = 2

    def_item_counts = [
        10, 50, 100, 500, 1000
    ]

    def __init__(self, conn, rtt_obj_model, page, items_per_page, address,
                 default_item_count=10, near_pages=2):
        self.default_item_count = default_item_count
        self.near_pages = near_pages
        self.address = address
        if self.address.endswith('/'):
            self.address += '?'

        # Page number validation
        try:
            self.page = int(page)
        except ValueError:
            self.page = 1

        # Items per page validation
        try:
            self.items_per_page = int(items_per_page)
        except ValueError:
            self.items_per_page = self.default_item_count
        if self.items_per_page < self.min_item_count:
            self.items_per_page = self.min_item_count
        if self.items_per_page > self.max_item_count:
            self.items_per_page = self.max_item_count

        total_items = rtt_obj_model.get_all_count(conn)
        min_total_page = 1
        max_total_page = int(ceil(total_items / self.items_per_page))

        # Correct value of page is ensured here
        self.page = max(min_total_page, self.page)
        self.page = min(max_total_page, self.page)

        min_near_page = max(min_total_page, self.page - self.near_pages)
        max_near_page = min(max_total_page, self.page + self.near_pages)

        self.pages = []
        for i in range(min_near_page, max_near_page + 1):
            self.pages.append(i)

        if min_total_page < min_near_page:
            self.first = min_total_page
        else:
            self.first = None

        if min_total_page < self.page:
            self.previous = self.page - 1
        else:
            self.previous = None

        if max_total_page > max_near_page:
            self.last = max_total_page
        else:
            self.last = None

        if max_total_page > self.page:
            self.next = self.page + 1
        else:
            self.next = None

        # Fetching objects that will be shown in template
        self.object_list = rtt_obj_model.get_some(
            conn, (self.page - 1) * self.items_per_page, self.items_per_page)

    def get_item_count_picker(self):
        if self.def_item_counts is None:
            return ''

        rval = '''
        <form role="form" class="form-inline">
        <div class="form-group">
        <label for="item_count">Items per page</label>
        <select id="item_count" title="Items per page" class="form-control">
        '''

        for ic in self.def_item_counts:
            if ic == self.items_per_page:
                rval += '''
                <option value="{0}" selected>{0}</option>
                '''.format(ic)
            else:
                rval += '''
                <option value="{0}">{0}</option>
                '''.format(ic)

        rval += '''
        </select>
        </div>
        <div class="btn-group">
        <a id="apply_btn" class="btn btn-default" onclick="setLinkItemCount('apply_btn');"
        href="{}page=1">
        Apply
        </a>
        </div>
        </form>
        '''.format(self.address)

        return rval

    def get_pagination_links(self):
        dots_str = '''
        <li class="disabled"><a>...</a></li>
        '''
        a_tag_str = '''
        <a href="{0}page={1}" id="{2}" onclick="setLinkItemCount('{2}')">{3}</a>
        '''
        link_str = '''
        <li>
        {}
        </li>
        '''.format(a_tag_str)
        link_active_str = '''
        <li class="active">
        {}
        </li>
        '''.format(a_tag_str)

        # Starting to build return html
        rval = '''
        <div class="text-center">
        <ul class="pagination pagination-lg">
        '''
        # Previous button
        if self.previous is not None:
            rval += link_str.format(self.address, self.previous, 'l_prev', '&lsaquo;')

        # First button
        if self.first is not None:
            rval += link_str.format(self.address, self.first, 'l_first', self.first)
            if self.first != self.pages[0] - 1:
                rval += dots_str

        # Buttons in between
        for p in self.pages:
            if p == self.page:
                rval += link_active_str.format(self.address, p, 'l_{}'.format(p), p)
            else:
                rval += link_str.format(self.address, p, 'l_{}'.format(p), p)

        # Last button
        if self.last is not None:
            if self.last != self.pages[-1] + 1:
                rval += dots_str

            rval += link_str.format(self.address, self.last, 'l_last', self.last)

        # Next button
        if self.next is not None:
            rval += link_str.format(self.address, self.next, 'l_next', '&rsaquo;')

        # Close tags
        rval += '''
        </ul>
        </div>
        '''
        # Append needed script
        rval += '''
        <script language="JavaScript">
            function setLinkItemCount(link_id) {
                var chosen = document.getElementById("item_count").value;
                if (chosen == null)
                    return;
                var val = document.getElementById(link_id).getAttribute("href");
                val += "&item_count=" + chosen;
                document.getElementById(link_id).setAttribute("href", val);
            }
        </script>
        '''

        # Not horribly easy to read I would say.
        return rval
