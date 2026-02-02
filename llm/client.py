"""
LLM Client for InsightX Exchange
Handles communication with Groq API for AI-powered insights
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
from utils.config import OPENAI_API_KEY, OPENAI_BASE_URL, DEFAULT_MODEL, TEMPERATURE, MAX_TOKENS


class LLMClient:
    """
    Client for interacting with Groq API for LLM functionality
    """
    
    def __init__(self):
        """Initialize the LLM client with API configuration"""
        self.api_key = OPENAI_API_KEY
        self.base_url = OPENAI_BASE_URL
        self.model = DEFAULT_MODEL
        self.temperature = TEMPERATURE
        self.max_tokens = MAX_TOKENS
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests
        
        # Set up headers for API requests
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def _enforce_rate_limit(self):
        """Enforce minimum time between requests to prevent rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        
        self.last_request_time = time.time()
    
    def generate_response(
        self, 
        prompt: str, 
        context: Optional[str] = None,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a response from the LLM
        
        Args:
            prompt: The main prompt/question
            context: Optional context to include
            system_prompt: Optional system prompt for behavior guidance
            max_tokens: Optional override for max tokens
            
        Returns:
            str: Generated response
        """
        try:
            # Construct messages
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add context if provided
            if context:
                messages.append({"role": "system", "content": f"Context: {context}"})
            
            # Add main prompt
            messages.append({"role": "user", "content": prompt})
            
            # Prepare API request
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": self.temperature,
                "max_tokens": max_tokens or self.max_tokens
            }
            
            # Make API request with enhanced rate limiting
            self._enforce_rate_limit()
            
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    response = requests.post(url, headers=self.headers, json=payload, timeout=30)
                    response.raise_for_status()
                    break  # Success, exit retry loop
                except requests.exceptions.HTTPError as e:
                    if "429" in str(e):
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = 2 ** retry_count  # Exponential backoff: 2s, 4s, 8s
                            time.sleep(wait_time)
                            continue
                        else:
                            return "⚠️ API rate limit exceeded. Please wait a moment and try again."
                    else:
                        raise
                except requests.exceptions.Timeout:
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(1)
                        continue
                    else:
                        return "⏰ Request timeout. Please try again."
            
            # Extract and return response
            result = response.json()
            return result["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            return f"API Error: {str(e)}"
        except KeyError as e:
            return f"Response parsing error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def analyze_trading_data(self, ticker: str, data: Dict[str, Any]) -> str:
        """
        Generate trading analysis insights
        
        Args:
            ticker: Stock ticker symbol
            data: Trading data and indicators
            
        Returns:
            str: Trading analysis insights
        """
        system_prompt = """You are an expert financial analyst specializing in stock market analysis. 
        Provide professional, educational insights about trading data. Focus on explaining technical indicators 
        and their implications in simple terms. Always include educational disclaimers."""
        
        prompt = f"""
        Analyze the following trading data for {ticker}:
        
        Current Price: ${data.get('current_price', 'N/A')}
        RSI: {data.get('rsi', 'N/A')}
        MACD: {data.get('macd', 'N/A')}
        Moving Averages: {data.get('moving_averages', 'N/A')}
        Volatility: {data.get('volatility', 'N/A')}
        
        Please provide:
        1. Technical analysis summary
        2. Key insights from indicators
        3. Educational explanation of what these indicators mean
        4. Risk considerations
        """
        
        return self.generate_response(prompt, system_prompt=system_prompt)
    
    def analyze_marketing_data(self, campaign_data: List[Dict[str, Any]]) -> str:
        """
        Generate marketing analysis insights
        
        Args:
            campaign_data: List of campaign performance data
            
        Returns:
            str: Marketing analysis insights
        """
        system_prompt = """You are an expert marketing analyst specializing in digital marketing campaigns. 
        Provide professional, educational insights about marketing performance metrics. Focus on explaining 
        KPIs and their implications in simple terms. Always include educational disclaimers."""
        
        # Format campaign data for analysis
        data_summary = "\n".join([
            f"Campaign: {campaign.get('campaign', 'Unknown')}, "
            f"Budget: ${campaign.get('budget', 0):,.2f}, "
            f"Revenue: ${campaign.get('revenue', 0):,.2f}, "
            f"ROI: {campaign.get('roi', 0):.2f}%, "
            f"Conversion Rate: {campaign.get('conversion_rate', 0):.2f}%"
            for campaign in campaign_data
        ])
        
        prompt = f"""
        Analyze the following marketing campaign data:
        
        {data_summary}
        
        Please provide:
        1. Performance analysis summary
        2. Key insights from the metrics
        3. Educational explanation of what these KPIs mean
        4. Recommendations for optimization
        """
        
        return self.generate_response(prompt, system_prompt=system_prompt)
    
    def generate_executive_summary(self, analysis_type: str, data: Dict[str, Any]) -> str:
        """
        Generate executive summary for reports
        
        Args:
            analysis_type: Type of analysis (trading/marketing)
            data: Analysis data
            
        Returns:
            str: Executive summary
        """
        system_prompt = """You are an expert business analyst. Generate concise, professional executive 
        summaries for business reports. Focus on key findings, implications, and actionable insights."""
        
        if analysis_type == "trading":
            prompt = f"""
            Generate an executive summary for this trading analysis:
            
            Ticker: {data.get('ticker', 'N/A')}
            Analysis Period: {data.get('period', 'N/A')}
            Key Findings: {data.get('key_findings', 'N/A')}
            Risk Assessment: {data.get('risk_assessment', 'N/A')}
            """
        else:  # marketing
            prompt = f"""
            Generate an executive summary for this marketing analysis:
            
            Campaigns Analyzed: {data.get('campaign_count', 'N/A')}
            Total Budget: ${data.get('total_budget', 0):,.2f}
            Total Revenue: ${data.get('total_revenue', 0):,.2f}
            Average ROI: {data.get('avg_roi', 0):.2f}%
            Key Findings: {data.get('key_findings', 'N/A')}
            """
        
        return self.generate_response(prompt, system_prompt=system_prompt)
    
    def chat_response(self, message: str, language: str = 'en') -> str:
        """
        Generate chatbot response with topic restrictions
        
        Args:
            message: User message
            language: Language preference ('en' or 'ar')
            
        Returns:
            str: Chatbot response
        """
        # Topic restriction system
        allowed_topics = ['marketing', 'trading', 'finance']
        message_lower = message.lower()
        
        # Check if message contains allowed topics
        topic_found = any(topic in message_lower for topic in allowed_topics)
        
        if not topic_found:
            return "it's out of you"
        
        system_prompt = f"""You are a helpful AI assistant for the InsightX Exchange platform. 
        You specialize in marketing and trading analytics. Be educational, professional, and helpful.
        Respond in {language if language == 'en' else 'Arabic'}.
        
        IMPORTANT: Only respond to messages related to marketing, trading, or finance.
        If a user message is NOT related to these topics, respond with exactly: "it's out of you"
        Do not provide explanations or ask clarifying questions for out-of-scope topics."""
        
        return self.generate_response(message, system_prompt=system_prompt)
    
    def health_check(self) -> bool:
        """
        Check if the LLM API is accessible
        
        Returns:
            bool: True if API is accessible, False otherwise
        """
        try:
            url = f"{self.base_url}/models"
            response = requests.get(url, headers=self.headers)
            return response.status_code == 200
        except:
            return False


# Global instance for easy access
llm_client = LLMClient()

# Export the client
__all__ = ['LLMClient', 'llm_client']