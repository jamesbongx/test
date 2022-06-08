#include "include.h"
#include "func.h"

static bool pause = 0;
widget_para_t btnImg[]={{UI_BUF_SPORT_PAUSE_BIN,0, 0, 52, 132, 46, 46},
						{UI_BUF_SPORT_START_BIN,0, 0, 52, 132, 46, 46},
						{UI_BUF_SPORT_EXIT_BIN, 0, 0,142, 132, 46, 46}
};
tp_pos_t tp_start;
int checkButton(widget_para_t *btn, tp_pos_t pos){
	for(int i = 0; i < 3; i++){
		if(pos.x >= btn[i].x2 && pos.y >= btn[i].y2){
			if(pos.x <= btn[i].x2 + btn[i].width && pos.y <= btn[i].y2 + btn[i].height){
				return i;
			}
		}
	}
	return -1;
}
void zxhd_sport_start_stop_touch_move_callback(void *page_ptr, tp_cb_t *tp_cb)
{
    tp_start = tp_cb->tp_start;
//	printf("%s:%x\n",__func__,tp_cb->tp_status);
	comm_touch_move_callback(page_ptr, tp_cb);
}

void zxhd_sport_start_stop_touch_release_callback(void *page_ptr, u8 release_type)
{
	int x = checkButton(btnImg, tp_start);
	printf("%s:%d:%d\n", __func__, release_type, x);
	if(release_type){
		comm_touch_release_callback(page_ptr, release_type);
	}
}

void zxhd_sport_start_stop_btn_touch_release_callback(void *btn_ptr, u8 release_type)
{
	if (release_type) {
		comm_touch_release_callback(btn_ptr, release_type);
		return;
	}
    widget_button_t *btn = btn_ptr;
	printf("%s:%x:%x\n",__func__, pause, btn->click_para);
	if (btn->click_para == 1) {
		if(pause){
			gui_break_jump(func_cb.sta, FUNC_ZXHD_SPORT_CONFIRM);
		}else{
			gui_break_jump(func_cb.sta, FUNC_GSPORT_COL);
		}
	} else {
		pause = !pause;
        gui_widget_set(btn_gui[0], &btnImg[pause], WGT_TYPE_BTN);
		gui_refresh();
	}
}

AT(.text.func.zxhd_sport)
void *lcd_zxhd_sport_start_stop_init(int x,int y)
{
	void *page_ptr = gui_create_backpage(x, y, 1);
	widget_page_set_callback(page_ptr, NULL, &zxhd_sport_start_stop_touch_release_callback , &zxhd_sport_start_stop_touch_move_callback);

	void *text = widget_creat(page_ptr, WGT_TYPE_TXT);
    gui_text_set_content(text, RUNNING_STR_1 + sys_cb.sport_index, TEXT_DESC_X, TEXT_DESC_Y,TEXT_DESC_COLOR, TEXT_BACK_COLOR, gui_cb.lang, false);

    for(int i = 0; i < 2; i++){
        btn_gui[i] = widget_creat(page_ptr, WGT_TYPE_BTN);
        gui_widget_set(btn_gui[i], &btnImg[i+ 1], WGT_TYPE_BTN);
		if(!sys_cb.gui_exit) {
			widget_button_set_callback(btn_gui[i], NULL, &zxhd_sport_start_stop_btn_touch_release_callback, NULL, i);
		}
    }

	widget_set_visible(page_ptr, true);
	gui_refresh();

	return page_ptr;
}

AT(.text.func.zxhd_sport)
void func_zxhd_sport_start_stop_process(void)
{
    func_process();
    func_watch_bt_process();
}

AT(.text.func.zxhd_sport)
static void func_zxhd_sport_start_stop_enter(void)
{
	pause = 0;
	page_gui = lcd_zxhd_sport_start_stop_init(0,0);
}

AT(.text.func.zxhd_sport)
static void func_zxhd_sport_start_stop_exit(void)
{
    gui_clr();

    if(!func_cb.sta_break){
        func_cb.last = FUNC_ZXHD_SPORT_STARTSTOP;
    }
}

AT(.text.func.zxhd_sport)
void func_zxhd_sport_start_stop(void)
{
	printf("%s\n", __func__);

	func_zxhd_sport_start_stop_enter();

	while (func_cb.sta == FUNC_ZXHD_SPORT_STARTSTOP){
		func_zxhd_sport_start_stop_process();
        func_message(msg_dequeue());
	}

	func_zxhd_sport_start_stop_exit();
}
