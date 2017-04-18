from math import ceil


class RTTPaginator(object):
    default_page = 1
    default_item_count = 10
    near_pages = 2
    min_item_count = 1
    # Unsigned big int (2^64)
    max_item_count = 18446744073709551615

    def_item_counts = [
        10, 50, 100, 500, 1000
    ]

    def __init__(self, request, conn, rtt_obj_model,
                 default_item_count=None, near_pages=None,
                 object_list=None, url_args=None):
        # Setting defaults
        if default_item_count is not None:
            self.default_item_count = default_item_count
        if near_pages is not None:
            self.near_pages = near_pages

        # Treating address
        self.address = request.path
        if url_args is not None:
            self.address += url_args

        if self.address.endswith('/'):
            self.address += '?'
        else:
            self.address += '&'

        # Processing request
        # Page number validation
        page = request.GET.get('page', self.default_page)
        try:
            self.page = int(page)
        except ValueError:
            self.page = 1

        # Items per page validation
        items_per_page = request.GET.get('item_count', self.default_item_count)
        try:
            self.items_per_page = int(items_per_page)
        except ValueError:
            self.items_per_page = self.default_item_count
        if self.items_per_page < self.min_item_count:
            self.items_per_page = self.min_item_count
        if self.items_per_page > self.max_item_count:
            self.items_per_page = self.max_item_count

        if object_list is None:
            # Getting total count from database
            total_items = rtt_obj_model.get_all_count(conn)
        else:
            # We already have the objects
            total_items = len(object_list)

        min_total_page = 1
        max_total_page = int(ceil(total_items / self.items_per_page))

        # Correct value of page is ensured here
        self.page = max(min_total_page, self.page)
        self.page = min(max_total_page, self.page)
        if self.page == 0:
            self.page = 1

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

        if object_list is None:
            # Fetching objects that will be shown in template
            self.object_list = rtt_obj_model.get_some(
                conn, (self.page - 1) * self.items_per_page, self.items_per_page)
        else:
            # Objects were provided, so just take correct part of them
            self.object_list = object_list[
                               (self.page - 1) * self.items_per_page:
                               (self.page - 1) * self.items_per_page + self.items_per_page]

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
        <a href="{0}page={1}&item_count=''' + str(self.items_per_page)
        a_tag_str += '''
        ">{2}</a>
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

        prev_arrow = self.page
        next_arrow = self.page

        # Starting to build return html
        rval = '''
        <div class="text-center">
        <ul class="pagination pagination-lg">
        '''
        # Previous button
        if self.previous is not None:
            prev_arrow = self.previous
            rval += link_str.format(self.address, self.previous, '&lsaquo;')

        # First button
        if self.first is not None:
            rval += link_str.format(self.address, self.first, self.first)
            if self.first != self.pages[0] - 1:
                rval += dots_str

        # Buttons in between
        for p in self.pages:
            if p == self.page:
                rval += link_active_str.format(self.address, p, p)
            else:
                rval += link_str.format(self.address, p, p)

        # Last button
        if self.last is not None:
            if self.last != self.pages[-1] + 1:
                rval += dots_str

            rval += link_str.format(self.address, self.last, self.last)

        # Next button
        if self.next is not None:
            next_arrow = self.next
            rval += link_str.format(self.address, self.next, '&rsaquo;')

        # Close tags
        rval += '''
        </ul>
        <span class="help-block">You can navigate between pages using arrow keys.</span>
        </div>
        '''
        # Append needed scripts
        rval += '''
        <script language="JavaScript">
            function setLinkItemCount(link_id) {{
                var chosen = document.getElementById("item_count").value;
                if (chosen == null)
                    return;
                var val = document.getElementById(link_id).getAttribute("href");
                val += "&item_count=" + chosen;
                document.getElementById(link_id).setAttribute("href", val);
            }}

            document.onkeydown = function(e) {{
                switch (e.keyCode) {{
                    case 37:
                        window.location.href = "{0}page={2}&item_count={1}";
                        break;
                    case 39:
                        window.location.href = "{0}page={3}&item_count={1}";
                        break;
                }}
            }};
        </script>
        '''.format(self.address, self.items_per_page, prev_arrow, next_arrow)

        # Not horribly easy to read I would say. But you will manage.
        return rval
