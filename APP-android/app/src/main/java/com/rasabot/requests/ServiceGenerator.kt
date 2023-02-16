package com.rasabot.requests

import com.rasabot.util.Constants
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object ServiceGenerator {

    val retrofitBuilder: Retrofit.Builder = Retrofit.Builder()
        .baseUrl(Constants.BASE_URL)
        .addConverterFactory(GsonConverterFactory.create())

    val CHAT_BOT_API: ChatBotApi by lazy {
        retrofitBuilder.build()
            .create(ChatBotApi::class.java)
    }

}