                                    gpt_response,
                                    self.config.AI_CHATTER.CHANNEL_ID,
                                    self.config.AI_CHATTER.GUILD_ID,
                                    message.message_id,
                                )

                                if ok:
                                    logger.success(
                                        f"{self.account.index} | 回复我的消息已发送: {gpt_response}"
                                    )
                                    self.my_account_id = json_response["author"]["id"]
                                    self.my_account_username = json_response["author"][
                                        "username"
                                    ]
                                    # 保存我们刚刚回复的消息ID
                                    self.my_replies_messages.append(message.message_id)
                                    message_sent, replied_to_me = True, True
                            else:
                                logger.info(
                                    f"{self.account.index} | 由于 answer_percentage，跳过回复"
                                )

                    if not replied_to_me:
                        # 如果没有人回复我们或我们还没有发送任何消息，
                        # 继续进行正常的回复逻辑
                        replyable_messages = [
                            msg
                            for msg in last_messages
                            if msg.referenced_message_content
                            and msg.author_username
                            != self.my_account_username  # 不要回复自己的消息
                        ]

                        # 根据百分比和可用消息确定是否应该回复
                        should_reply = (
                            (random.random() * 100)
                            < self.config.AI_CHATTER.REPLY_PERCENTAGE
                            and replyable_messages
                        )

                        if should_reply:
                            # 发送回复消息给某人
                            message = random.choice(replyable_messages)
                            logger.info(
                                f"{self.account.index} | 发送回复消息给 {message.author_username}。主消息: {message.content}。引用的消息: {message.referenced_message_content}"
                            )
                            gpt_response = await self._deepseek_referenced_messages(
                                message.content,
                                message.referenced_message_content,
                            )
                            gpt_response = (
                                gpt_response.replace("```", "")
                                .replace("```python", "")
                                .replace("```", "")
                                .replace('"', "")
                            )

                            random_pause = random.randint(
                                self.config.AI_CHATTER.PAUSE_BEFORE_MESSAGE[0],
                                self.config.AI_CHATTER.PAUSE_BEFORE_MESSAGE[1],
                            )
                            logger.info(
                                f"{self.account.index} | GPT 回复: {gpt_response}。发送消息前暂停 {random_pause} 秒。"
                            )

                            await asyncio.sleep(random_pause)
                            ok, json_response = await self._send_message(
                                gpt_response,
                                self.config.AI_CHATTER.CHANNEL_ID,
                                self.config.AI_CHATTER.GUILD_ID,
                                message.message_id,
                            )

                            if ok:
                                logger.success(
                                    f"{self.account.index} | 回复消息已发送: {gpt_response}"
                                )
                                self.my_account_id = json_response["author"]["id"]
                                message_sent = True

                        else:
                            # 根据聊天历史发送简单消息
                            messages_contents = "| ".join(
                                [message.content for message in last_messages]
                            )
                            # logger.info(
                            #     f"{self.account.index} | 消息内容: {messages_contents}"
                            # )

                            gpt_response = await self._deepseek_batch_messages(
                                messages_contents,
                            )
                            gpt_response = (
                                gpt_response.replace("```", "")
                                .replace("```python", "")
                                .replace("```", "")
                                .replace('"', "")
                            )

                            random_pause = random.randint(
                                self.config.AI_CHATTER.PAUSE_BEFORE_MESSAGE[0],
                                self.config.AI_CHATTER.PAUSE_BEFORE_MESSAGE[1],
                            )
                            logger.info(
                                f"{self.account.index} | GPT 回复: {gpt_response}。发送消息前暂停 {random_pause} 秒。"
                            )
                            await asyncio.sleep(random_pause)

                            ok, json_response = await self._send_message(
                                gpt_response,
                                self.config.AI_CHATTER.CHANNEL_ID,
                                self.config.AI_CHATTER.GUILD_ID,
                            )

                            if ok:
                                logger.success(
                                    f"{self.account.index} | 未回复的消息已发送: {gpt_response}"
                                )
                                self.my_account_id = json_response["author"]["id"]
                                message_sent = True

                    if message_sent:
                        random_pause = random.randint(
                            self.config.AI_CHATTER.PAUSE_BETWEEN_MESSAGES[0],
                            self.config.AI_CHATTER.PAUSE_BETWEEN_MESSAGES[1],
                        )
                        logger.info(
                            f"{self.account.index} | 发送下一条消息前暂停 {random_pause} 秒。"
                        )
                        await asyncio.sleep(random_pause)
                        break

                    else:
                        random_pause = random.randint(
                            self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[0],
                            self.config.SETTINGS.PAUSE_BETWEEN_ATTEMPTS[1],
                        )
                        logger.info(
                            f"{self.account.index} | 没有发送消息。重试前暂停 {random_pause} 秒。"
                        )
                        await asyncio.sleep(random_pause)

                except Exception as e:
                    logger.error(f"{self.account.index} | start_chatting 出错: {e}")
                    return False

    async def _send_message(
        self,
        message: str,
        channel_id: str,
        guild_id: str,
        reply_to_message_id: str = None,
    ) -> tuple[bool, dict]:
        try:
            headers = {
                "authorization": self.account.token,
                "content-type": "application/json",
                "origin": "https://discord.com",
                "referer": f"https://discord.com/channels/{guild_id}/{channel_id}",
                "x-debug-options": "bugReporterEnabled",
                "x-discord-locale": "en-US",
                "x-discord-timezone": "Etc/GMT-2",
                # 'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InJ1IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMT[...]
            }

            json_data = {
                "mobile_network_type": "unknown",
                "content": message,
                "nonce": calculate_nonce(),
                "tts": False,
                "flags": 0,
            }

            if reply_to_message_id:
                json_data["message_reference"] = {
                    "guild_id": guild_id,
                    "channel_id": channel_id,
                    "message_id": reply_to_message_id,
                }

            response = await self.client.post(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                headers=headers,
                json=json_data,
            )

            return response.status_code == 200, response.json()

        except Exception as e:
            logger.error(f"{self.account.index} | send_message 出错: {e}")
            return False, None

    async def _get_last_chat_messages(
        self, guild_id: str, channel_id: str, quantity: int = 50
    ) -> list[str]:
        try:

            headers = {
                "authorization": self.account.token,
                "referer": f"https://discord.com/channels/{guild_id}/{channel_id}",
                "x-discord-locale": "en-US",
                "x-discord-timezone": "Etc/GMT-2",
                # 'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6InJ1IiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMT[...]
            }

            params = {
                "limit": str(quantity),
            }

            response = await self.client.get(
                f"https://discord.com/api/v9/channels/{channel_id}/messages",
                params=params,
                headers=headers,
            )

            if response.status_code != 200:
                logger.error(
                    f"get_last_chat_messages 出错: {response.status_code}"
                )
                return []

            received_messages = []
            for message in response.json():
                try:
                    if (
                        "you just advanced to level" in message["content"]
                        or message["content"] == ""
                    ):
                        continue

                    message_data = ReceivedMessage(
                        type=message["type"],
                        content=message["content"],
                        message_id=message["id"],
                        channel_id=message["channel_id"],
                        author_id=message["author"]["id"],
                        author_username=message["author"]["username"],
                        referenced_message_content=(
                            ""
                            if message.get("referenced_message") in ["None", None]
                            else message.get("referenced_message", {}).get(
                                "content", ""
                            )
                        ),
                        referenced_message_author_id=(
                            ""
                            if message.get("referenced_message") in ["None", None]
                            else message.get("referenced_message", {})
                            .get("author", {})
                            .get("id", "")
                        ),
                    )
                    received_messages.append(message_data)
                except Exception as e:
                    continue

            return received_messages

        except Exception as e:
            logger.error(
                f"{self.account.index} | get_last_chat_messages 出错: {e}"
            )
            return []

    async def _gpt_referenced_messages(
        self, main_message_content: str, referenced_message_content: str
    ) -> str:
        """
        使用GPT生成对引用消息的回复
        """
        try:
            user_message = f"""以前的消息: "{referenced_message_content}"
                回复此消息: "{main_message_content}"
                生成一个自然的回复继续这个对话。
            """

            ok, gpt_response = ask_chatgpt(
                random.choice(self.config.CHAT_GPT.API_KEYS),
                self.config.CHAT_GPT.MODEL,
                user_message,
                GPT_REFERENCED_MESSAGES_SYSTEM_PROMPT,
                proxy=self.config.CHAT_GPT.PROXY_FOR_CHAT_GPT,
            )

            if not ok:
                raise Exception(gpt_response)

            return gpt_response
        except Exception as e:
            logger.error(
                f"{self.account.index} | chatter _gpt_referenced_messages 出错: {e}"
            )
            raise e

    async def _deepseek_referenced_messages(
        self, main_message_content: str, referenced_message_content: str
    ) -> str:
        """
        使用DeepSeek生成对引用消息的回复，如果失败则使用ChatGPT
        """
        try:
            api_key = random.choice(self.config.DEEPSEEK.API_KEYS)
            user_message = f"消息1: {referenced_message_content}\n消息2: {main_message_content}"
            
            success, response = await ask_deepseek(
                api_key=api_key,
                model=self.config.DEEPSEEK.MODEL,
                user_message=user_message,
                prompt=DEEPSEEK_REFERENCED_MESSAGES_SYSTEM_PROMPT,
                proxy=self.config.DEEPSEEK.PROXY_FOR_DEEPSEEK,
            )
            
            if not success:
                logger.warning(f"{self.account.index} | DeepSeek API失败，切换到ChatGPT: {response}")
                return
                # return await self._gpt_referenced_messages(main_message_content, referenced_message_content)
                
            return response
        except Exception as e:
            logger.warning(f"{self.account.index} | DeepSeek错误，切换到ChatGPT: {str(e)}")
            return
            # return await self._gpt_referenced_messages(main_message_content, referenced_message_content)

    async def _gpt_batch_messages(self, messages_contents: list[str]) -> str:
        """
        使用GPT基于聊天历史生成新消息
        """
        try:
            user_message = f"""
                聊天记录: {messages_contents}
            """

            ok, gpt_response = ask_chatgpt(
                random.choice(self.config.CHAT_GPT.API_KEYS),
                self.config.CHAT_GPT.MODEL,
                user_message,
                GPT_BATCH_MESSAGES_SYSTEM_PROMPT,
                proxy=self.config.CHAT_GPT.PROXY_FOR_CHAT_GPT,
            )

            if not ok:
                raise Exception(gpt_response)

            return gpt_response
        except Exception as e:
            logger.error(
                f"{self.account.index} | chatter _gpt_batch_messages 出错: {e}"
            )
            raise e

    async def _deepseek_batch_messages(self, messages_contents: str) -> str:
        """
        使用DeepSeek基于聊天历史生成新消息，如果失败则使用ChatGPT
        """
        try:
            api_key = random.choice(self.config.DEEPSEEK.API_KEYS)
            
            success, response = await ask_deepseek(
                api_key=api_key,
                model=self.config.DEEPSEEK.MODEL,
                user_message=messages_contents,
                prompt=DEEPSEEK_BATCH_MESSAGES_SYSTEM_PROMPT,
                proxy=self.config.DEEPSEEK.PROXY_FOR_DEEPSEEK,
            )
            
            if not success:
                logger.warning(f"{self.account.index} | DeepSeek API失败，切换到ChatGPT: {response}")
                return
                # return await self._gpt_batch_messages(messages_contents)
                
            return response
        except Exception as e:
            logger.warning(f"{self.account.index} | DeepSeek错误，切换到ChatGPT: {str(e)}")
            return 
            # return await self._gpt_batch_messages(messages_contents)
