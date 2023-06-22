package com.rasabot.requests

import com.rasabot.models.BotMessage
import com.rasabot.models.Message
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface ChatBotApi {

    @POST("webhook")
    fun messageBot(@Body userMessage: Message): Call<ArrayList<BotMessage>>
}