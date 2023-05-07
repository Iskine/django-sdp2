from django import template

register = template.Library()

@register.simple_tag
def get_user_role(user):
    if user.groups.filter(name='team_manager').exists():
        return 'Dean'
    elif user.groups.filter(name='team_leader').exists():
        return 'Advisor'
    elif user.groups.filter(name='team_member').exists():
        return 'Student'
    else:
        return 'Admin'
