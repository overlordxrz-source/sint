#include "csi_handler.h"
#include "esp_timer.h"
#include "lwip/sockets.h"
#include <string.h>

#define HOST_IP   "192.168.100.28"
#define HOST_PORT 5005
#define MAX_CSI_LEN 128

static int udp_sock = -1;
static struct sockaddr_in dest_addr;

void csi_callback(void *ctx, wifi_csi_info_t *info) {
    if (!info || !info->buf) return;

    // Build packet: [timestamp_ms:8][rssi:1][noise:1][ch:1][n_sc:1][csi:2*n_sc]
    uint8_t pkt[8 + 4 + MAX_CSI_LEN * 2];
    uint64_t ts = esp_timer_get_time() / 1000;
    memcpy(pkt, &ts, 8);
    pkt[8]  = (uint8_t)(-info->rx_ctrl.rssi);     // store as positive
    pkt[9]  = (uint8_t)(-info->rx_ctrl.noise_floor);
    pkt[10] = info->rx_ctrl.channel;
    pkt[11] = info->len / 2;  // num complex samples (I+Q each int8)
    
    int csi_len = info->len;
    if (csi_len > MAX_CSI_LEN * 2) {
        csi_len = MAX_CSI_LEN * 2;
        pkt[11] = MAX_CSI_LEN;
    }
    memcpy(pkt + 12, info->buf, csi_len);

    sendto(udp_sock, pkt, 12 + csi_len, 0,
           (struct sockaddr *)&dest_addr, sizeof(dest_addr));
}

// Call once before enabling CSI:
void init_udp_socket(void) {
    udp_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    dest_addr.sin_family      = AF_INET;
    dest_addr.sin_port        = htons(HOST_PORT);
    inet_aton(HOST_IP, &dest_addr.sin_addr);
}

void ping_task(void *pvParam) {
    // Send UDP ping to router every 20 ms to drive CSI rate up to ~50 Hz
    int sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    struct sockaddr_in router = {
        .sin_family = AF_INET, .sin_port = htons(9)  // discard port
    };
    inet_aton("192.168.100.1", &router.sin_addr);  // router IP (assuming .1)
    while (1) {
        sendto(sock, "p", 1, 0, (struct sockaddr *)&router, sizeof(router));
        vTaskDelay(pdMS_TO_TICKS(20));
    }
}
