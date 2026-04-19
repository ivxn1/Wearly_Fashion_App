from django.http import HttpResponseBadRequest


class SetPaginateByMixin:
    def get_paginate_by(self, queryset):
        if "per-page" in self.request.GET:
            try:
                new_paginate_by = int(self.request.GET.get("per-page"))
                if new_paginate_by > 0:
                    self.request.session["paginate_by"] = new_paginate_by
            except (TypeError, ValueError):
                raise HttpResponseBadRequest

        return self.request.session.get("paginate_by", self.paginate_by)


class IsUserOwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)
