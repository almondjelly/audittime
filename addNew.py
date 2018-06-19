from model import Category


def goal_generate_html(total_time, goal_id, goal_name, goal_type, days, hours,
                       minutes, start_time, end_time, time_left, goal_status,
                       all_categories, goal_category):
    """Generates html for adding new goal."""

    html = ""

    html += "<tr class=\"tr-goal\">\
\
        <!-- Goal id -->\
        <form class=\"form-goal-id\"><input type=\"hidden\" class=\"input-goal-id\" value=\"{goal_id}\"></form>\
\
            <!-- Goal name -->\
            <td class=\"td-goal-name\" data-toggle=\"modal\" data-target=\"#{goal_id}-modal\">{goal_name}</td>\
\
            <!-- Goal type -->\
            <td class=\"td-goal-type\" data-toggle=\"modal\" data-target=\"#{goal_id}-modal\">for ".format(goal_id=goal_id, goal_name=goal_name)

    if goal_type == "at_least":
        html += "at least"

    elif goal_type == "at_most":
        html += "at most"

    html += "</td>\
\
            <!-- Goal duration target -->\
            <td class=\"td-goal-duration\" data-toggle=\"modal\" data-target=\"#{goal_id}-modal\">".format(goal_id=goal_id)

    if days > 0:
        html += "{}d ".format(days)

    if hours > 0:
        html += "{}h ".format(hours)

    if minutes > 0:
        html += "{}min ".format(minutes)

    html += "</td>\
\
            <!-- Goal end -->\
            <td class=\"td-goal-end-time\" data-toggle=\"modal\" data-target=\"#{goal_id}-modal\">\
                by {end_time}".format(goal_id=goal_id, end_time=end_time.strftime('%b %d at %I:%M %p'))
    
    html += "</td>\
\
            <!-- Goal total time progress -->\
            <td class=\"td-goal-total-time\" data-toggle=\"modal\" data-target=\"#{goal_id}-modal\">".format(goal_id=goal_id)
    
    html += " {}".format(total_time)

    html += "</td>\
\
            <!-- Goal time left -->\
            <td class=\"td-goal-time-left\" data-toggle=\"modal\" data-target=\"#{goal_id}-modal\"> {time_left}".format(goal_id=goal_id, time_left=time_left)
    
    html += "</td>\
\
            <!-- Goal status -->\
            <td class=\"td-goal-status\" data-toggle=\"modal\" data-target=\"#{goal_id}-modal\">".format(goal_id=goal_id)

    if goal_status == "Success!":
        html += "<span class=\"success\">{}</span>".format(goal_status)

    elif goal_status == "FAILED":
        html += "<span class=\"fail\">{}</span>".format(goal_status)

    elif goal_status == "In progress":
        html += "{}".format(goal_status)

    html += "</td>\
\
            <!-- Archive -->\
            <td class=\"td-goal-archive\">\
                <span class=\"span-goal-archive\">\
                <button type=\"button\" class=\"btn btn-link btn-goal-archive\">\
                    x\
                </button>\
                </span>\
\
            <!-- Edit modal -->\
            <div class=\"modal fade\" id=\"{goal_id}-modal\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"modalLabel\" aria-hidden=\"true\">".format(goal_id=goal_id)
    
    html += "<div class=\"modal-dialog\" role=\"document\">\
                <div class=\"modal-content\">\
                <div class=\"modal-header\">\
                    <h5 class=\"modal-title\" id=\"modalLabel\">Edit Goal</h5>\
                    <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\">\
                        <span aria-hidden=\"true\">&times;</span>\
                    </button>\
                </div>\
\
                <div class=\"modal-body\">\
                <form class=\"modal-form\">\
\
               <table>\
\
                <!-- Goal name -->\
                <tr class=\"tr-goal-modal-name\">\
                    <td class=\"goal-modal\">Goal</td>\
                    <td class=\"td-goal-modal-input\">\
                        <input class=\"goal-modal-input-name\" type=\"text\" value=\"{goal_name}\" name=\"{goal_id}\">".format(goal_name=goal_name, goal_id=goal_id)

    html += "</td>\
                </tr>\
\
                <!-- Goal type -->\
                <tr class=\"tr-goal-modal-type\">\
                <td class=\"goal-modal\">Type</td>\
                <td class=\"td-goal-modal-input\">\
                    <select class=\"goal-modal-input-type\">"

    if goal_type == "at_least":
        html += "<option value=\"at_least\" selected>at least</option>\
                <option value=\"at_most\">at most</option>"

    else:
        html += "<option value=\"at_least\">at least</option>\
                <option value=\"at_most\" selected>at most</option>"

    html += "</select>\
                </td>\
                </tr>\
\
                <!-- Goal target duration -->\
                <tr class=\"tr-goal-modal-target\">\
                <td class=\"goal-modal\">Target</td>\
                <td class=\"td-goal-modal-input\">\
                \
                <!-- Days -->\
                <input class=\"goal-modal-input-duration days\" type=\"text\" value=\"{days}\" name=\"days-{goal_id}\"> days<br>".format(days=days, goal_id=goal_id)

    html += "<!-- Hours -->\
                <input class=\"goal-modal-input-duration hours\" type=\"text\" value=\"{hours}\" name=\"hours-{goal_id}\"> hours and<br>".format(hours=hours, goal_id=goal_id)

    html += "<!-- Minutes -->\
                <input class=\"goal-modal-input-duration minutes\" type=\"text\" value=\"{minutes}\" name=\"minutes-{goal_id}\"> minutes".format(minutes=minutes, goal_id=goal_id)

    html += "</td>\
                </tr>\
\
                <!-- Goal start -->\
                <tr class=\"tr-goal-modal-start\">\
                <td class=\"goal-modal\">Start</td>\
                <td class=\"td-goal-modal-input\">\
                    <span class=\"goal-start-time time-text\">{}".format(start_time.strftime('%b %d at %I:%M %p'))

    html += "</span>\
                    <span class=\"input-goal-start-time time-input\">\
                        <input type=\"datetime-local\" class=\"modal-input-goal-date-time-picker\"> \
                    </span>\
                </td>\
                </tr>\
\
                <!-- Goal end -->\
                <tr class=\"tr-goal-modal-end\">\
                    <td class=\"goal-modal\">End</td>\
                    <td class=\"td-goal-modal-input\">\
                        <span class=\"goal-end-time time-text\">{}".format(end_time.strftime('%b %d at %I:%M %p'))

    html += "</span>\
                        <span class=\"input-goal-end-time time-input\">\
                            <input type=\"datetime-local\" name=\"endDate\" class=\"modal-input-goal-date-time-picker\">\
                        </span>\
                    </td>\
                </tr>\
\
                <!-- Goal categories -->\
                <tr class=\"tr-goal-modal-categories\">\
                    <td class=\"goal-modal\">Categories</td>\
                    <td class=\"td-goal-modal-input\">\
                        <select multiple class=\"goal-modal-input-goal-categories\">"

    for category in all_categories:
        if category in goal_category:
            html += "<option selected>{category_name}</option>".format(category_name=category.name)

        else:
            html += "<option>{category_name}</option>".format(category_name=category.name)


    html += "</select>\
                    </td>\
                </tr>\
\
                </table>\
                </div>\
\
                <div class=\"modal-footer\">\
                    <button type=\"button\" class=\"btn btn-link goal-edit-save\">Save</button>\
                </div>\
            </form>\
\
            </div>\
            </div>\
            </div>\
            </div>\
\
\
            </td>\
        </tr>"

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