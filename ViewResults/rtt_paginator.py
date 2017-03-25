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

    def __init__(self, conn, rtt_obj_model, page, items_per_page,
                 default_item_count=10, near_pages=2):
        self.default_item_count = default_item_count
        self.near_pages = near_pages

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
