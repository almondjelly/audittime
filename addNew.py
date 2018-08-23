from model import Category

def goal_generate_html(goal_id, 
                       goal_name,
                       categories,
                       goal_categories, 
                       goal_type, 
                       start_time, 
                       end_time,
                       days, 
                       hours,
                       minutes,
                       target,
                       total_time,
                       time_left, 
                       goal_status):
    """Generate html for adding new goal."""

    html = ""

    html += '<div class="goal-row row">\
            <div class="col-sm-12">\
\
                <!-- Goal id -->\
                <form class="form-goal-id"><input type="hidden" class="input-goal-id" value="{goal_id}"></form>'.format(goal_id=goal_id)

    html += '<div class="row">\
                    <div class="col-sm-7"><div class="row">\
\
                        <div class="col-sm-1 goal-expand">\
                            <i class="material-icons expand-more">expand_more</i>\
                        </div>\
\
                        <!-- Goal name -->\
                        <div class="col-sm-3 goal-name">\
                            <input type="text" value="{goal_name}" class="goal-name">'.format(goal_name=goal_name)

    html += '</div>\
\
                        <!-- Goal categories -->\
                        <div class="col-sm-2 goal-categories">\
                            <select class="goal-categories" multiple>'

    for category in categories:
        if category in goal_categories:
            html += '<option value="{category_name}" selected="selected">{category_name}</option>'.format(category_name=category.name)

        else:
            html += '<option value="{category_name}">{category_name}</option>'.format(category_name=category.name)
                                  
    html += '</select>\
                        </div>\
\
                        <!-- Goal type -->\
                        <div class="col-sm-2 goal-type">\
                            <select class="goal-type">\
                                <option selected class="option-goal-type-selected">'
                                    
    if goal_type == "at_least":
        html += 'at least'
    
    else:
        html += 'at most'

    html += '</option>\
                                <option class="option-goal-type-unselected">'

    if goal_type == "at_least":
        html += 'at most'

    else:
        html += 'at least'

    html += '</option>\
                            </select>\
\
                        </div>\
\
                        <!-- Goal time range -->\
                        <div class="col-sm-4 goal-range">\
                            <input hidden value="{start_time}" class="goal-range-start">'.format(start_time=start_time)
    html += '<input hidden value="{end_time}" class="goal-range-end">'.format(end_time=end_time)
    
    html += '<input name="datetimes" type="text" class="goal-range">\
                        </div>\
\
                    </div></div>\
\
                    <div class="col-sm-5"><div class="row">\
\
                        <div class="col-sm-11"><div class="row">\
                            <!-- Goal duration target -->\
                            <div class="col-sm-3 goal-target">'

    if days > 0:
        html += "{days}d ".format(days=days)

    if hours > 0:
        html += "{hours}h ".format(hours=hours)

    if minutes > 0:
        html += "{minutes}min ".format(minutes=minutes)

    html += '<input type="text" class="goal-target">\
\
                            </div>\
\
                            <!-- Goal total time progress -->\
                            <div class="col-sm-3 goal-total-time">\
                                {total_time}'.format(total_time=total_time)
                            
    html += '</div>\
\
                            <!-- Goal time left -->\
                            <div class="col-sm-3 goal-time-left">\
                                {time_left}'.format(time_left=time_left)

    html += '</div>\
\
                            <!-- Goal status -->\
                            <div class="col-sm-3 goal-status">'

    if goal_status == 'Success!':
        html += '<span class="success">{goal_status}</span>'.format(goal_status=goal_status)

    elif goal_status == 'FAILED':
        html += '<span class="fail">{goal_status}</span>'.format(goal_status=goal_status)

    elif goal_status == 'In progress':
        html += '{goal_status}'.format(goal_status=goal_status)
                                
    html += '</div>\
                        </div></div>\
\
                        <!-- Archive -->\
                        <div class="col-sm-1 goal-archive"><div class="row">\
                            <span class="span-goal-archive">\
                            </span>\
                        </div></div>\
                    </div></div>\
                </div>\
            </div>\
        </div>'

    return html


def category_generate_html(category_id, category_name, all_goals,
                           category_goal):
    """Generates html for adding a new category."""

    html1 = "<tr class=\"tr-category\"> \
    <form class=\"form-category-id\"> \
        <!-- Category id --> \
        <input type=\"hidden\" class=\"input-category-id\" value=\"{category_id}\"> \
        <!-- Category name --> \
        <td class=\"td-category\"> \
            <input type=\"text\" value=\"{category_name}\" name=\"{category_id}\" class=\"td-input-category\"> \
        </td> \
        <!-- Category goals --> \
        <td class=\"td-category-goals\"> \
            <select multiple class=\"td-input-category-goals\">".format(
                category_name=category_name, category_id=category_id)

    html2 = ''.format()

    for goal in all_goals:
        if goal in category_goal:
            html2 += "<option selected>{}</option>".format(goal.name)
        else:
            html2 += "<option>{}</option>".format(goal.name)

    html3 = "</select> \
        </td> \
        <!-- Save --> \
        <td class=\"td-category-save\"> \
        <span class=\"span-category-save\"> \
            <button class=\"btn btn-primary\"><i class=\"material-icons\">save</i></button> \
        </span> \
        </td> \
        <!-- Archive --> \
        <td class=\"td-category-archive\"> \
        <span class=\"span-category-archive\"> \
            <button class=\"btn btn-primary btn-category-archive\"><i class=\"material-icons\">clear</i></button> \
        </span> \
        </td> \
    </form> \
    </tr>"

    new_category_html = html1 + html2 + html3

    return new_category_html


def timer_generate_html(event_id, timer_id, timer_name, category_name,
                       all_categories, start, stop, duration):

    new_timer_html = '<tr class="tr-event-timer"> \
\
        <!-- Event id, timer id --> \
        <form class="form-event-id"> \
            <input type="hidden" class="input-event-id" value={}>\
            <input type="hidden" class="input-timer-id" value={}>\
        </form>'.format(event_id, timer_id)

    new_timer_html += '<!-- Task name -->\
        <td class="td-event-timer">\
            <input type="text" value="{}" class="td-input-event-timer">\
        </td>'.format(timer_name)

    new_timer_html += '<!-- Category dropdown -->\
        <td class="td-event-timer-categories">\
            <select class="td-input-event-timer-categories">\
                <option selected>{}</option>'.format(category_name)

    for category in all_categories:
        new_timer_html += '<option>{}</option>'.format(category.name)

    new_timer_html += '</select>\
        </td>\
\
        <!-- Start and end times -->\
        <td class="td-event-start-time">\
            {}\
            <input type="datetime-local" class="input-timer-start-date-time-picker">\
        </td>\
\
        <td class="td-event-end-time">\
            {}\
            <input type="datetime-local" class="input-timer-end-date-time-picker">\
        </td>'.format(start, stop)

    new_timer_html += '<!-- Duration -->\
        <td class="td-event-duration">\
            {}\
        </td>\
\
        <!-- Save -->\
        <td class="td-event-timer-save">\
        <span class="span-event-timer-save">\
            <button class="btn btn-link btn-event-timer-save">save</button>\
        </span>\
        </td>\
\
        <!-- Delete -->\
        <td class="td-event-timer-remove">\
        <span class="span-event-timer-remove">\
            <button class="btn btn-link btn-event-timer-remove">x</button>\
        </span>\
        </td>\
\
    </form>\
    </tr>'.format(duration)

    return new_timer_html