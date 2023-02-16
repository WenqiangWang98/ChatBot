package com.rasabot.util

class Constants {

    companion object {
        val NGROCK_URL = "http://chatbots.ieef.upm.es:5008"
        val BASE_URL = "$NGROCK_URL/webhooks/rest/"
        val NETWORK_TIMEOUT = 5000L
        val MESSAGE_TEXT_NULL = "NA"

        val USER = 0
        val BOT = 1
        val LOADING = 2
    }
}