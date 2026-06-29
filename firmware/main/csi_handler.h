#ifndef CSI_HANDLER_H
#define CSI_HANDLER_H

#include "esp_wifi.h"

void init_udp_socket(void);
void csi_callback(void *ctx, wifi_csi_info_t *info);
void ping_task(void *pvParam);

#endif // CSI_HANDLER_H
