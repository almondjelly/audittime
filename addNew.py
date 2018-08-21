from model import Category

def goal_generate_html(goal_id, 
                       goal_name, 
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

    html += '<table class="goal-log"> \
            <tr class="tr-goal"> \
    \
                <!-- Goal id -->\
                <form class="form-goal-id"><input type="hidden" class="input-goal-id" value="{goal_id}"></form>'.format(goal_id=goal_id)

    html += '           <td class="td-goal-expand">\
                    <i class="material-icons expand-more">expand_more</i>\
                </td>\
    \
                <!-- Goal name -->\
                <td class="td-goal-name">\
                    <input type="text" value="{goal_name}" class="td-input-goal-name">'.format(goal_name=goal_name)
            
    html += '</td>\
    \
                <!-- Goal type -->\
                <td class="td-goal-type">\
                    <select class="select-goal-type">\
                        <option selected class="option-goal-type-selected">'

    if goal_type == "at_least":
        html += 'at least'

    elif goal_type == "at_most":
        html += 'at most'

    html += '                    </option>\
                        <option class="option-goal-type-unselected">'

    if goal_type == "at_least":
        html += 'at most'

    else:
        html += 'at least'
                            
    html += '                    </option>\
                    </select>\
    \
                </td>\
    \
                <!-- Goal time range -->\
                <td class="td-goal-range">\
                    <input hidden value="{start_time}" class="td-goal-range-start">\
                    <input hidden value="{end_time}" class="td-goal-range-end">'.format(start_time=start_time, end_time=end_time)

    html += '                <input name="datetimes" type="text" class="td-input-goal-range">\
                </td>\
    \
                <!-- Goal duration target -->\
                <td class="td-goal-duration">'

    if days > 0:
        html += "{days}d ".format(days=days)

    if hours > 0:
        html += "{hours}h ".format(hours=hours)

    if minutes > 0:
        html += "{minutes}min ".format(minutes=minutes)

    html += '   <input type="text" class="td-input-goal-target">'

    html += '</td>\
\
                <!-- Goal total time progress -->\
                <td class="td-goal-total-time">\
                    {total_time}'.format(total_time=total_time)
    
    html += '            </td>\
\
                <!-- Goal time left -->\
                <td class="td-goal-time-left">\
                    {time_left}'.format(time_left=time_left)

    html += '            </td>\
\
                <!-- Goal status -->\
                <td class="td-goal-status">'

    if goal_status == 'Success!':
        html += '<span class="success">{goal_status}</span>'.format(goal_status=goal_status)

    elif goal_status == 'FAILED':
        html += '<span class="fail">{goal_status}</span>'.format(goal_status=goal_status)

    elif goal_status == 'In progress':
        html += '{goal_status}'.format(goal_status=goal_status)

    html += '            </td>\
\
                <!-- Archive -->\
                <td class="td-goal-archive">\
                    <span class="span-goal-archive">\
                        \
                    </span>\
                </td>\
            </tr>\
        </table>'

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


def task_generate_html(event_id, task_id, task_name, category_name,
                       all_categories, start, stop, duration):

    new_task_html = '<tr class="tr-event-task"> \
\
        <!-- Event id, task id --> \
        <form class="form-event-id"> \
            <input type="hidden" class="input-event-id" value={}>\
            <input type="hidden" class="input-task-id" value={}>\
        </form>'.format(event_id, task_id)

    new_task_html += '<!-- Task name -->\
        <td class="td-event-task">\
            <input type="text" value="{}" class="td-input-event-task">\
        </td>'.format(task_name)

    new_task_html += '<!-- Category dropdown -->\
        <td class="td-event-task-categories">\
            <select class="td-input-event-task-categories">\
                <option selected>{}</option>'.format(category_name)

    for category in all_categories:
        new_task_html += '<option>{}</option>'.format(category.name)

    new_task_html += '</select>\
        </td>\
\
        <!-- Start and end times -->\
        <td class="td-event-start-time">\
            {}\
            <input type="datetime-local" class="input-task-start-date-time-picker">\
        </td>\
\
        <td class="td-event-end-time">\
            {}\
            <input type="datetime-local" class="input-task-end-date-time-picker">\
        </td>'.format(start, stop)

    new_task_html += '<!-- Duration -->\
        <td class="td-event-duration">\
            {}\
        </td>\
\
        <!-- Save -->\
        <td class="td-event-task-save">\
        <span class="span-event-task-save">\
            <button class="btn btn-link btn-event-task-save">save</button>\
        </span>\
        </td>\
\
        <!-- Delete -->\
        <td class="td-event-task-remove">\
        <span class="span-event-task-remove">\
            <button class="btn btn-link btn-event-task-remove">x</button>\
        </span>\
        </td>\
\
    </form>\
    </tr>'.format(duration)

    return new_task_html