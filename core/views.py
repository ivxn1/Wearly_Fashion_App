"""
Views for the core application.

This module contains class-based views for the main pages of the application,
including the home page and about page.
"""

from django.views.generic import TemplateView
from django.utils.timezone import localdate

from outfits.models import Outfit
from planner.models import PlanEntry
from wardrobe.models import Garment


class HomeView(TemplateView):
    """
    Display the home page with recent garments, outfits, and upcoming plans.

    Shows the 3 most recent items from each category.
    """

    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Wearly Home'
        context['wardrobe'] = Garment.objects.select_related('brand').order_by('-created_at')[:3]
        context['outfits'] = Outfit.objects.order_by('-created_at')[:3]
        context['plans'] = PlanEntry.objects.select_related('outfit').filter(date__gte=localdate()).order_by('date')[:3]
        return context


class AboutView(TemplateView):
    """
    Display the about page with application information and contact details.
    """

    template_name = 'core/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Wearly'
        context['main'] = ('Wearly is a lightweight outfit planning web application that helps '
                           'you stay organized when it comes to clothing and daily outfit choices.')
        context['secondary'] = ('Instead of keeping outfits in your head or scattered notes, Wearly lets you store wardrobe, '
                                'create outfits from them, and plan what to wear for upcoming days — all in one place.')
        context['contacts'] = 'If you have questions or suggestions, feel free to reach out at:'
        context['email'] = 'contact@wearly.app'
        return context
